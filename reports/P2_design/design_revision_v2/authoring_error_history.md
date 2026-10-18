# Document authoring error history

Initial specification-builder invocation failed with TypeError: dict() got multiple values for keyword argument classification.
The root provenance label classification=PROPOSED collided with a nested load-classification contract field.
The failed original script is preserved as spec_builder_initial.py.txt. CMD-008 reproduces the real error (exit1, raw stderr retained);
CMD-009 after renaming the nested field to load_classification exits0. This is a document-authoring failure, not a scientific/P1 test failure.
No production code, prior proposal or gate was modified.

CMD-021 fresh review actually returned1:301 checks passed and A_BEFORE_B_NO_RELABELLING failed.
The check searched one exact English phrasing while v2 already stated the same deterministic policy in
other wording. To remove prose ambiguity, matrix now exposes an explicit selection_policy object
(A/B order,B2,all10 seeds,own target,retain-all,no relabel/no deletion,no effect-based selection).
The check now verifies those fields. This is a checker/specification formalization correction, not a
change to selection values or scientific outcomes. Initial checker/result and raw command exits retained.

CMD-033 added delivery-metadata review exited1 before producing JSON: a Path join was accidentally
written as subscripting (R[path]). Its actual traceback and initial checker are preserved. The caller
also emitted JSONDecodeError while attempting to parse the empty stdout; that wrapper failure is
not an additional recorded subprocess. Correcting to R/path changes only the metadata checker, not
any proposal, source or research rule. This is disclosed separately from scientific/P1 tests.

CMD-034 after the Path fix produced31 checks:30PASS,1FAIL. The reviewer incorrectly expected18
human-packet hash references. Actual packet has16 references to13 affected files, all hashes match.
The extra five v2 documents (indexes/overview/registry/trace/checklist) are covered by full manifest
and traceability rather than each decision's affected-file list. Corrected only the reference-count
expectation to16/13. Failed JSON/second checker/raw command outputs retained.
