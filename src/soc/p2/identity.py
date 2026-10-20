"""Closed identity schemas, exact canonicalization and immutable artifact IO."""
from __future__ import annotations

from fractions import Fraction
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import struct


class EvidenceError(ValueError):
    pass


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def semantic_bytes(value) -> bytes:
    def check(v):
        if v is None or type(v) in (bool, int):
            return
        if type(v) is str:
            if not v.isascii():
                raise EvidenceError('non-ASCII semantic string')
            return
        if type(v) is list:
            for x in v:
                check(x)
            return
        if type(v) is dict and all(type(k) is str and k.isascii() for k in v):
            for x in v.values():
                check(x)
            return
        raise EvidenceError('semantic object contains float/unsupported type')
    check(value)
    return (json.dumps(value, sort_keys=True, ensure_ascii=True,
                       separators=(',', ':'), allow_nan=False)+'\n').encode()


def strict_json(data: bytes):
    def pairs(rows):
        result = {}
        for key, value in rows:
            if key in result:
                raise EvidenceError('duplicate JSON key')
            result[key] = value
        return result
    def invalid(value):
        raise EvidenceError('nonfinite JSON token: '+value)
    return json.loads(data, object_pairs_hook=pairs, parse_constant=invalid)


def rational(value: Fraction) -> dict:
    value = Fraction(value)
    return {'numerator': str(value.numerator), 'denominator': str(value.denominator)}


def fraction(value: dict) -> Fraction:
    if not isinstance(value, dict) or set(value) != {'numerator', 'denominator'}:
        raise EvidenceError('invalid rational fields')
    n, d = value['numerator'], value['denominator']
    if not isinstance(n, str) or not isinstance(d, str) or not re.fullmatch(r'0|-?[1-9][0-9]*', n) or not re.fullmatch(r'[1-9][0-9]*', d):
        raise EvidenceError('noncanonical rational')
    f = Fraction(int(n), int(d))
    if rational(f) != value:
        raise EvidenceError('rational not reduced')
    return f


def bits(value: float) -> str:
    if type(value) not in (int, float) or not math.isfinite(value) or value < 0:
        raise EvidenceError('invalid public binary64 number')
    return struct.pack('>d', float(value) if value else 0.0).hex()


def unbits(value: str) -> float:
    if not isinstance(value, str) or not re.fullmatch('[0-9a-f]{16}', value):
        raise EvidenceError('invalid binary64 encoding')
    number = struct.unpack('>d', bytes.fromhex(value))[0]
    if not math.isfinite(number) or number < 0 or bits(number) != value:
        raise EvidenceError('noncanonical/nonfinite binary64')
    return number


def safe_path(root: Path, relative: str) -> Path:
    p = PurePosixPath(relative)
    if (not isinstance(relative, str) or not relative.isascii() or '\\' in relative or
            p.is_absolute() or not p.parts or any(x in ('', '.', '..') for x in relative.split('/'))):
        raise EvidenceError('unsafe artifact path')
    root = root.resolve()
    target = root.joinpath(*p.parts)
    if not target.resolve().is_relative_to(root):
        raise EvidenceError('artifact escapes root')
    return target


def fsync_dir(path: Path):
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


class ArtifactStore:
    """Exclusive creation; conflicting bytes never overwrite existing evidence.

    Filesystem crash durability is a deployment property, not implied by fsync.
    This store is for a trusted authority; it is not a worker sandbox.
    """
    def __init__(self, root: Path):
        self.root = root.resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def put(self, relative: str, data: bytes, kind: str = 'EVIDENCE', media_type='application/json') -> dict:
        path = safe_path(self.root, relative)
        # Persist each newly created directory before publishing children.
        current = self.root
        for part in path.relative_to(self.root).parts[:-1]:
            child = current/part
            if not child.exists():
                child.mkdir()
                fsync_dir(current)
            if child.is_symlink():
                raise EvidenceError('symlink artifact directory')
            current = child
        try:
            fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        except FileExistsError:
            if path.is_symlink() or path.read_bytes() != data:
                raise EvidenceError('immutable artifact conflict: '+relative)
        else:
            with os.fdopen(fd, 'wb') as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
            fsync_dir(path.parent)
        return {'path': relative, 'sha256': digest(data), 'size_bytes': len(data),
                'media_type': media_type, 'kind': kind}

    def get(self, ref: dict) -> bytes:
        if set(ref) != {'path', 'sha256', 'size_bytes', 'media_type', 'kind'}:
            raise EvidenceError('invalid artifact reference fields')
        path = safe_path(self.root, ref['path'])
        if path.is_symlink():
            raise EvidenceError('symlink artifact')
        data = path.read_bytes()
        if type(ref['size_bytes']) is not int or len(data) != ref['size_bytes'] or digest(data) != ref['sha256']:
            raise EvidenceError('artifact hash/size mismatch')
        return data

    def inventory(self, refs: list[dict]) -> dict:
        refs = sorted(refs, key=lambda r: r['path'])
        if len({r['path'] for r in refs}) != len(refs):
            raise EvidenceError('duplicate inventory path')
        for ref in refs:
            self.get(ref)
        data = semantic_bytes(refs)
        return self.put('inventories/'+digest(data)+'.json', data, 'ARTIFACT_INVENTORY')


class Types:
    """Validator for the precise keyword vocabulary used by the bound schema.

    Unknown assertion keywords fail at construction, rather than being ignored.
    This checks structure; semantic relationships need independent predicates.
    """
    def __init__(self, path: Path):
        self.document = strict_json(path.read_bytes())
        self.defs = self.document['$defs']
        vocabulary = {'$ref', 'type', 'const', 'enum', 'properties', 'required',
                      'additionalProperties', 'items', 'minItems', 'maxItems',
                      'minimum', 'maximum', 'exclusiveMinimum', 'exclusiveMaximum',
                      'pattern', 'minLength', 'maxLength', 'anyOf', 'oneOf',
                      'description', 'title', 'uniqueItems'}
        def check(schema):
            if not isinstance(schema, dict):
                raise EvidenceError('unsupported schema shape')
            unknown = set(schema)-vocabulary
            if unknown:
                raise EvidenceError('unsupported schema keywords '+str(sorted(unknown)))
            for child in schema.get('properties', {}).values(): check(child)
            if isinstance(schema.get('items'), dict): check(schema['items'])
            for op in ('anyOf', 'oneOf'):
                for child in schema.get(op, []): check(child)
        for schema in self.defs.values(): check(schema)

    def validate(self, name: str, value):
        self._validate(self.defs[name], value)
        if name == 'RATIONAL': fraction(value)
        return value

    def identity(self, name: str, body: dict) -> tuple[str, str]:
        self.validate(name, body)
        registry = {**self.document['preimage_registry'], **self.document['v3_preimage_registry']}
        if name not in registry:
            raise EvidenceError('not a registered identity preimage')
        sha = digest(semantic_bytes(body))
        return registry[name]['id_prefix']+sha, sha

    def _validate(self, schema, value):
        if '$ref' in schema:
            prefix = '#/$defs/'
            if not schema['$ref'].startswith(prefix): raise EvidenceError('external schema ref')
            self._validate(self.defs[schema['$ref'][len(prefix):]], value)
        kind = schema.get('type')
        kinds = {'object': type(value) is dict, 'array': type(value) is list,
                 'string': type(value) is str, 'integer': type(value) is int,
                 'boolean': type(value) is bool, 'null': value is None,
                 'number': type(value) is int or (type(value) is float and math.isfinite(value))}
        if kind is not None and not any(kinds.get(k, False) for k in (kind if isinstance(kind, list) else [kind])):
            raise EvidenceError('wrong schema type '+str(kind))
        if 'const' in schema and (type(value) is not type(schema['const']) or value != schema['const']):
            raise EvidenceError('schema const mismatch')
        if 'enum' in schema and not any(type(value) is type(v) and value == v for v in schema['enum']):
            raise EvidenceError('schema enum mismatch')
        for op in ('anyOf', 'oneOf'):
            if op in schema:
                matches = 0
                for branch in schema[op]:
                    try: self._validate(branch, value)
                    except EvidenceError: pass
                    else: matches += 1
                if (op == 'anyOf' and matches == 0) or (op == 'oneOf' and matches != 1):
                    raise EvidenceError(op+' mismatch')
        if type(value) is dict:
            if not set(schema.get('required', [])) <= value.keys(): raise EvidenceError('missing required fields')
            props = schema.get('properties', {})
            if schema.get('additionalProperties') is False and not value.keys() <= props.keys():
                raise EvidenceError('unexpected fields')
            for k, v in value.items():
                if k in props: self._validate(props[k], v)
        if type(value) is list:
            if len(value) < schema.get('minItems', 0) or len(value) > schema.get('maxItems', float('inf')):
                raise EvidenceError('array length')
            if schema.get('uniqueItems') and len({json.dumps(x, sort_keys=True) for x in value}) != len(value):
                raise EvidenceError('duplicate array item')
            if 'items' in schema:
                for v in value: self._validate(schema['items'], v)
        if type(value) is str:
            if len(value) < schema.get('minLength', 0) or len(value) > schema.get('maxLength', float('inf')):
                raise EvidenceError('string length')
            if 'pattern' in schema and re.search(schema['pattern'], value) is None: raise EvidenceError('string pattern')
        if type(value) in (int, float):
            for op, predicate in [('minimum', lambda x: value >= x), ('maximum', lambda x: value <= x),
                                  ('exclusiveMinimum', lambda x: value > x), ('exclusiveMaximum', lambda x: value < x)]:
                if op in schema and not predicate(schema[op]): raise EvidenceError('numeric bound')
