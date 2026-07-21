# CrossFit Business Copilot Blind Laboratory

## Objective

Validate whether two independent implementations created from the same frozen
input can be compared reproducibly through blind evaluation.

## Method

- same frozen project input;
- same ShapingTheAxe kernel;
- isolated candidate worktrees;
- frozen candidate results;
- anonymised evaluation packages;
- three independent evaluations;
- adversarial verification;
- final meta-analysis.

## Result

- neither candidate triggered a hard failure;
- all three evaluators preferred Candidate X;
- Candidate X showed stronger functional correctness and proportionality;
- Candidate Y showed stronger API-analysis depth and review transparency;
- evaluator-generated adversarial checks found defects missed by candidate-owned
  test suites.

## Main conclusion

This experiment provides positive beta evidence that ShapingTheAxe can support
controlled execution, reproducible candidate freezing, blind comparative
evaluation and independent handoff.

It does not prove universal effectiveness.

## Main artifacts

- `blind-evaluation/`
- `packages/`
- `protocol/`
- `final-evidence/`
- `private/IDENTITY_MAP.md`
- `crossfit-business-copilot-final-evidence.tar.gz`
