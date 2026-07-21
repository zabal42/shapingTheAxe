# Business

Esta carpeta contiene la exploración de negocio construida sobre
ShapingTheAxe. **No es normativa para el framework.** Si algo aquí entra en
conflicto con `SHAPING_THE_AXE_BRAIN_SPEC.md` o `ShapingTheAxe.md`, esos dos
archivos gobiernan; esta carpeta describe hipótesis y decisiones de producto,
no reglas de comportamiento del kernel.

## Estado de cada documento

| Documento | Naturaleza | Estado |
|---|---|---|
| [`VISION.md`](VISION.md) | Visión estratégica | No validada; fases futuras no implican alcance del MVP |
| [`ELDORADO_HYPOTHESIS.md`](ELDORADO_HYPOTHESIS.md) | Hipótesis de producto | Ambiciosa, no validada; incluye criterios explícitos de refutación; el nivel 3 ("Tres niveles") contenía una contradicción entre fuentes, resuelta por decisión de autoridad de producto — ver esa sección para la resolución y su justificación |
| [`STA_ASSISTANTS_FOUNDATION.md`](STA_ASSISTANTS_FOUNDATION.md) | Documento fundador | Borrador para validación |
| [`PRODUCT_HYPOTHESES.md`](PRODUCT_HYPOTHESES.md) | Hipótesis de modelo de producto | Candidatas, orden de validación recomendado |
| [`BUSINESS_MODELS.md`](BUSINESS_MODELS.md) | Modelos de negocio posibles | Recomendación provisional |
| [`MVP_VALIDATION.md`](MVP_VALIDATION.md) | Protocolo de validación del MVP | Diseñado, pendiente de ejecución completa |
| [`DECISIONS.md`](DECISIONS.md) | Registro de decisiones | Mezcla de aprobado, abierto y candidato — ver estado de cada entrada |

## `history/`

Documentos fuente originales, retirados de uso activo pero conservados
verbatim por trazabilidad. Ninguno se edita; cada consolidado enlaza a su(s)
histórico(s):

| Histórico | Procedencia | Por qué se conserva |
|---|---|---|
| [`history/ELDORADO_HYPOTHESIS.origin-sta-assistants.md`](history/ELDORADO_HYPOTHESIS.origin-sta-assistants.md) | `STA/STA-Assistant/.../ELDORADO_HYPOTHESIS.md` | Fuente de la fusión en `ELDORADO_HYPOTHESIS.md`; formulaba el nivel 3 como "Generación avanzada", distinto de la otra fuente — contradicción ya resuelta allí por autoridad de producto |
| [`history/ELDORADO_HYPOTHESIS.origin-crossfit-lab.md`](history/ELDORADO_HYPOTHESIS.origin-crossfit-lab.md) | `Chatbots_Whatsapp_Pymes/docs/vision/ELDORADO_HYPOTHESIS.md` | Idem; formulaba el nivel 3 como "Generación autónoma" |
| [`history/STA_ASSISTANTS_README.origin.md`](history/STA_ASSISTANTS_README.origin.md) | `STA/STA-Assistant/.../README.md` | Prosa fundacional (propósito, pregunta central, hipótesis principal) que este índice no reproduce |

## Relación con `validation/`

El primer caso de validación comparativa ejecutado bajo este dominio de
negocio (CrossFit Business Copilot) vive en
[`../validation/case-studies/crossfit-business-copilot/`](../validation/case-studies/crossfit-business-copilot/).
Ese caso prueba el protocolo ShapingTheAxe en general; no valida por sí solo
ninguna de las hipótesis de negocio de esta carpeta.

## Criterio de honestidad

Igual que exige `STA_ASSISTANTS_FOUNDATION.md`: distinguir siempre entre
visión, hipótesis, decisión, evidencia y resultado demostrado. Ningún
documento de esta carpeta se trata como validado solo porque esté escrito con
detalle.
