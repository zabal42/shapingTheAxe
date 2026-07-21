# Meta-Evaluation of the CrossFit Business Copilot Blind Experiment

## 1. Purpose

This document compares three independent blind evaluations of Candidate X and
Candidate Y.

It does not re-evaluate the candidates directly.

Its purpose is to identify:

- conclusions shared across evaluators;
- material disagreements;
- reproducible confirmed defects;
- limitations in the evaluation process;
- evidence relevant to the validation of ShapingTheAxe.

## 2. Evaluation reports

1. `../evaluations/01_Informe_Evaluacion_Ciega_claude.pdf`
2. `../evaluations/02_Informe_Evaluacion_Ciega_ChatGptWork.md`
3. `../evaluations/03_Informe_Evaluacion_Ciega_ClaudeCode_opus.md`

## 3. Comparative result

| Measure | Evaluation 01 | Evaluation 02 | Evaluation 03 |
|---|---:|---:|---:|
| Hard failures in X | 0 | 0 | 0 |
| Hard failures in Y | 0 | 0 | 0 |
| Preferred candidate | X | X | X |
| Score X | 92/100 | Ranking confirmed | 90/100 |
| Score Y | 79/100 | Ranking confirmed | 82/100 |
| Difference considered material | Yes | Yes | Moderate but real |

## 4. Consensus findings

| Finding | Eval 01 | Eval 02 | Eval 03 | Consensus |
|---|---|---|---|---|
| Candidate X is stronger overall | Yes | Yes | Yes | 3/3 |
| Neither candidate triggers a hard failure | Yes | Yes | Yes | 3/3 |
| Candidate Y mishandles capacity-zero sessions | Yes | Yes | Yes | 3/3 |
| Candidate Y ignores explicit date ranges | Yes | Yes | Yes | 3/3 |
| Candidate Y models inactivity using reservations rather than attendance | Yes | Yes | Yes | 3/3 |
| Candidate Y has stronger API discovery documentation | Yes | Yes | Yes | 3/3 |
| Candidate Y has stronger transparency about its internal review | Yes | Yes | Yes | 3/3 |
| Candidate X is more proportional in fixture size | Yes | Yes | Yes | 3/3 |

## 5. Additional findings

### 5.1 Candidate X

Evaluation 03 found that Candidate X does not recognise the literal phrase
“menor ocupación” from US-02.

This issue was not reported by Evaluations 01 or 02 and therefore has a current
consensus level of 1/3.

### 5.2 Candidate Y

The following defects were reproduced by multiple evaluators:

- capacity-zero sessions are included silently in occupancy averages;
- explicit date ranges are ignored;
- inactivity is based on reservations rather than actual attendance;
- cancelled sessions are not represented in the domain model.

## 6. Evaluation-process limitations

### 6.1 Missing evaluator evidence

Evaluation 01 referenced adversarial scripts that were not present in the
material later audited by Evaluation 02.

Evaluation 02 reproduced the central defects independently but could not verify
the exact stated adversarial totals.

### 6.2 Fixture-size correction

Evaluation 01 described Candidate Y's fixture as approximately 2.3 MB.

Evaluation 02 measured the three JSON files at approximately 1.57 MiB.

The proportionality conclusion remains valid, but the original figure should
be corrected.

### 6.3 Environment-specific Python limitation

Evaluation 01 reported that Python 3.11 was unavailable in its environment.

Evaluation 02 used Python 3.14.6, so this limitation was not reproduced and
must be treated as evaluator-environment-specific.

### 6.4 Substitute test runner

Evaluation 03 could not install pytest without network access and used a
self-validated substitute runner.

This weakens exact equivalence when reproducing Candidate Y's own suite, but
does not invalidate the directly executed adversarial findings.

## 7. Robust conclusions

1. Candidate X is the stronger product base.
2. The ranking is driven by functional correctness, not documentation or test
   volume.
3. Candidate Y contains reproducible correctness defects not detected by its
   own 57-test suite.
4. Candidate X is more faithful to inactivity based on actual attendance.
5. Candidate Y demonstrates stronger API-analysis depth and review
   transparency.
6. Both architectures are serious, reproducible and free from hard failures.
7. Independent adversarial evaluation adds substantial value beyond
   candidate-owned tests and self-assessment.

## 8. Implications for ShapingTheAxe

The experiment provides evidence that ShapingTheAxe can support:

- controlled equivalent starting conditions;
- provider-independent execution;
- explicit risk and scope control;
- traceable assumptions and contradictions;
- reproducible candidate freezing;
- blind evaluation;
- evaluator-generated adversarial checks;
- handoff independent of the original conversation.

The experiment also exposed improvement candidates:

- formal verification-repair loop;
- mandatory preservation of evaluator-generated evidence;
- clearer execution-artifact location rules;
- formal pause/resume states;
- stronger isolation against Git-reference leakage;
- calibration scenarios for “material” and “minimum sufficient”.

## 9. Overall verdict

The three evaluations converge on the same ranking and on the central reasons
for that ranking.

The exact scores vary, but the comparative conclusion is robust:

> Candidate X is materially stronger as a product baseline, while Candidate Y
> remains a technically serious implementation with better API-analysis depth
> and process transparency but several reproducible functional defects.

For ShapingTheAxe, this experiment should be treated as:

> positive multidomain beta evidence, not proof of universal effectiveness.

## 10. Confidence

- Confidence in the ranking: High
- Confidence in the central reproduced defects: High
- Confidence in exact numerical scores: Medium
- Confidence in universal claims about ShapingTheAxe: Low
