# Independent Blind Evaluation

Act as a clean independent evaluator.

You have two anonymous candidate packages:

- candidate-x.tar.gz
- candidate-y.tar.gz

Use only:

- the contents of those packages;
- EVALUATION_RUBRIC.md;
- evidence you reproduce yourself.

Do not use prior conversation context.
Do not infer or identify the runtime, model or tool that created either
candidate.
Do not reward code volume, documentation volume or test count by themselves.
Do not accept the candidates' own acceptance claims without verification.

Tasks:

1. Verify package integrity using the supplied hashes.
2. Inspect both candidates independently.
3. Install and execute each candidate using its own instructions.
4. Run each candidate's test suite.
5. Apply equivalent adversarial checks to both candidates.
6. Inspect architecture, API analysis, assumptions, limitations and handoff.
7. Apply every hard failure and scoring rule exactly as written.
8. Distinguish:
   - product defects;
   - documentation defects;
   - fixture limitations;
   - environment limitations;
   - unsupported claims.
9. Produce a complete comparative report.

Do not modify the candidate packages.
If additional tests or scripts are needed, create them outside the candidate
directories and report them as evaluator-generated evidence.

The final report must be understandable without access to the original
conversation.
