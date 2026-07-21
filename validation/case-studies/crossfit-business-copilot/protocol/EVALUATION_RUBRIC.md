# Blind Evaluation Rubric

## Purpose

Evaluate two anonymous implementations of the same CrossFit Business Copilot
MVP.

The evaluator must compare product quality only.

The evaluator must not infer or speculate about:

- the model or tool that created each candidate;
- the candidate identity;
- the development process;
- execution logs not included in the package.

Documentation volume, code volume and test count do not receive credit by
themselves.

Claims must be supported by inspected files, executed tests or reproducible
behaviour.

---

## Hard Failures

Any of the following produces an automatic FAIL:

1. A required MVP question cannot be answered.
2. Business figures are invented or calculated by a language model.
3. The candidate requires real AimHarder credentials to run.
4. The candidate modifies the frozen experiment input.
5. The candidate cannot be executed from the supplied instructions.
6. Core business calculations have no automated verification.
7. The candidate performs write operations against AimHarder or real business
   data.
8. The final handoff is materially misleading about verification or
   limitations.

---

## Scoring

Total: 100 points.

### 1. Functional correctness — 25 points

Evaluate:

- average occupancy;
- lowest-occupancy classes;
- cancellation rate by time slot;
- inactive active users;
- occupancy comparison between periods;
- handling of unsupported or ambiguous questions;
- correctness of edge cases.

Do not rely only on the candidate's own tests.

### 2. Determinism and reproducibility — 15 points

Evaluate:

- reproducible fixtures;
- stable dates and periods;
- deterministic ordering;
- absence of silent dependence on the current clock;
- repeatable commands and results;
- clean installation and execution.

### 3. Architecture and replaceability — 15 points

Evaluate whether:

- business metrics are separated from data access;
- a future AimHarder adapter can be introduced without rewriting the metric
  calculations;
- parsing, calculation and presentation responsibilities are appropriately
  separated;
- complexity is proportional to the MVP.

Do not reward named architectural patterns unless they materially improve the
result.

### 4. Explainability and prudence — 10 points

Every analytical answer should communicate as appropriate:

- metric definition;
- period;
- included data;
- exclusions;
- assumptions;
- limitations.

Evaluate whether the system refuses or clarifies unsupported questions rather
than inventing conclusions.

### 5. API understanding and traceability — 10 points

Evaluate:

- accurate use of the supplied AimHarder documentation;
- identified capabilities and gaps;
- visible contradictions;
- separation of documented behaviour from assumptions;
- future integration limitations.

### 6. Automated verification quality — 10 points

Evaluate:

- meaningful coverage of business rules;
- edge cases;
- regression quality;
- independence from implementation details;
- whether green tests genuinely support acceptance claims.

More tests do not automatically mean better verification.

### 7. Documentation and handoff — 10 points

Evaluate whether another developer can:

- understand the project;
- install and run it;
- verify the results;
- understand assumptions and residual risks;
- continue toward a real AimHarder integration.

### 8. Proportionality and maintainability — 5 points

Evaluate:

- unnecessary code, data or documentation;
- duplicated logic;
- avoidable dependencies;
- fixture size relative to the MVP;
- ease of future maintenance.

---

## Common Adversarial Checks

The evaluator should test both candidates with equivalent scenarios, including:

- empty dataset;
- period with no valid sessions;
- capacity equal to zero;
- cancelled bookings;
- waiting-list bookings;
- active user with no attendance;
- attendance linked to a cancelled session;
- explicit numeric zero;
- ambiguous period wording;
- two periods mentioned without a valid comparison;
- unsupported metric comparison;
- paraphrases from the user stories;
- deterministic ordering under repeated runs.

The evaluator may add further tests when justified, but must apply equivalent
checks to both candidates.

---

## Final Output

For each candidate provide:

- hard-failure result;
- score by dimension;
- total score;
- confirmed defects;
- unsupported claims;
- strengths;
- residual risks;
- reproducibility verdict.

Then provide:

- comparative verdict;
- which candidate is stronger and why;
- whether the difference is material;
- areas where neither candidate is satisfactory;
- confidence and limitations of the evaluation.

Do not reveal or guess candidate identities.
