> **Histórico — verbatim, no normativo.** Procedencia:
> `Chatbots_Whatsapp_Pymes/docs/vision/ELDORADO_HYPOTHESIS.md`, laboratorio
> externo, incorporado el 2026-07-21. No editar. Versión consolidada actual:
> [`../ELDORADO_HYPOTHESIS.md`](../ELDORADO_HYPOTHESIS.md).

---

# ELDORADO_HYPOTHESIS

> Hipótesis de producto surgida durante la conversación.

## Cambio de enfoque

El producto deja de ser:

> Crear un chatbot para una peluquería.

Y pasa a ser:

> Crear una fábrica gobernada por ShapingTheAxe capaz de diagnosticar un
> negocio y generar su asistente a medida.

## Idea central

El chatbot es copiable.

Lo diferencial es el proceso que convierte un negocio real en un
asistente útil:

-   entender qué hace;
-   detectar qué tareas merece automatizar;
-   decidir qué datos necesita;
-   separar lo obligatorio de lo accesorio;
-   diseñar tono y personalidad;
-   conectar agenda, clientes y servicios;
-   establecer límites;
-   verificar que no inventa;
-   dejarlo desplegable y mantenible.

## El MVP

No genera automáticamente un chatbot completo.

Genera una especificación ejecutable:

-   business-profile.yaml
-   assistant-policy.md
-   services.json
-   conversation-style.md
-   integration-config.yaml
-   acceptance-tests.md

Una plantilla común utiliza esos artefactos para construir el asistente.

## El verdadero foso

No es:

> Tenemos una IA que responde.

Es:

> Tenemos un protocolo que convierte un negocio real en un asistente
> operativo, controlado y verificable.

## Flujo

Negocio ↓ Entrevista / Documentos ↓ STA carga contexto ↓ Detecta
necesidades y riesgos ↓ Genera Business Profile ↓ Genera configuración ↓
Genera pruebas ↓ Instancia el asistente ↓ Verifica ↓ Entrega

## Tres niveles

1.  Configurador asistido.
2.  Diagnóstico inteligente.
3.  Generación autónoma.

## Conclusión

No construimos chatbots uno a uno.

Hemos creado un sistema que entiende cada negocio y genera su asistente.
