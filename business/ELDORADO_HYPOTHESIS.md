# Hipótesis Eldorado

**Estado:** hipótesis ambiciosa, no validada.

> Nota de fusión: este documento consolida dos redacciones independientes de
> la misma hipótesis, escritas en momentos distintos de la exploración.
> Ambas se conservan íntegras y sin editar como históricos:
>
> - [`history/ELDORADO_HYPOTHESIS.origin-sta-assistants.md`](history/ELDORADO_HYPOTHESIS.origin-sta-assistants.md)
> - [`history/ELDORADO_HYPOTHESIS.origin-crossfit-lab.md`](history/ELDORADO_HYPOTHESIS.origin-crossfit-lab.md)
>
> La mayor parte del contenido era complementaria y se combina sin conflicto.
> Una sección contenía una contradicción real entre las fuentes — ver "Tres
> niveles" más abajo. Esa contradicción fue resuelta por decisión explícita de
> la autoridad de producto, no por elección editorial de quien fusionó el
> documento; ambas formulaciones originales permanecen visibles en
> `history/` para que la comparación sea verificable.

## Cambio de enfoque

El producto deja de ser:

> Crear un chatbot para una peluquería.

Y pasa a ser:

> Crear una fábrica gobernada por ShapingTheAxe capaz de diagnosticar un
> negocio y generar su asistente a medida.

## Idea central

El chatbot es copiable.

Lo diferencial es el proceso que convierte un negocio real en un asistente
útil:

- entender qué hace;
- detectar qué tareas merece automatizar;
- decidir qué datos necesita;
- separar lo obligatorio de lo accesorio;
- diseñar tono y personalidad;
- conectar agenda, clientes y servicios;
- establecer límites;
- verificar que no inventa;
- dejarlo desplegable y mantenible.

## Tesis

La dificultad real no está solo en el chatbot final, sino en convertir un
negocio concreto en una definición operativa del asistente: necesidades,
reglas, excepciones, datos, tono, límites y criterios de verificación.

## El MVP

No genera automáticamente un chatbot completo.

Genera una especificación ejecutable:

- `business-profile.yaml`
- `assistant-policy.md`
- `services.json`
- `conversation-style.md`
- `integration-config.yaml`
- `acceptance-tests.md`

Una plantilla común utiliza esos artefactos para construir el asistente.

## Posible producto

Un sistema que transforma información del negocio en un paquete verificable
de definición del asistente.

## El verdadero foso

No es:

> Tenemos una IA que responde.

Es:

> Tenemos un protocolo que convierte un negocio real en un asistente
> operativo, controlado y verificable.

## Posible ventaja

El posible foso sería disponer de un método probado para convertir negocios
reales en asistentes fiables de forma repetible. Esa ventaja solo existe si
puede medirse.

## Flujo

Negocio → Entrevista / Documentos → STA carga contexto → Detecta necesidades
y riesgos → Genera Business Profile → Genera configuración → Genera pruebas →
Instancia el asistente → Verifica → Entrega

## Tres niveles

1. Configurador asistido.
2. Diagnóstico inteligente.
3. Generación agéntica avanzada con supervisión humana.

   **Resolución de autoridad de producto:** las dos fuentes originales
   formulaban este nivel de forma distinta y no sinónima —
   "Generación avanzada" (origen STA Assistants) frente a "Generación
   autónoma" (origen laboratorio CrossFit), donde "autónoma" sugería ausencia
   de supervisión humana y "avanzada" no lo especificaba. Tras comparar
   ambas fuentes, la autoridad de producto decidió la formulación anterior,
   que fija explícitamente la supervisión humana como parte del nivel 3 en
   lugar de dejarla implícita o ambigua. Ambas formulaciones originales
   permanecen sin editar en:
   - [`history/ELDORADO_HYPOTHESIS.origin-sta-assistants.md`](history/ELDORADO_HYPOTHESIS.origin-sta-assistants.md)
     ("Generación avanzada");
   - [`history/ELDORADO_HYPOTHESIS.origin-crossfit-lab.md`](history/ELDORADO_HYPOTHESIS.origin-crossfit-lab.md)
     ("Generación autónoma").

## Posibles compradores futuros

Agencias, consultoras, integradores, empresas SaaS, desarrolladores,
franquicias y equipos internos.

## Validación

La hipótesis gana fuerza si reduce tiempo, omisiones y retrabajo, aumenta
trazabilidad y personalización, y funciona con varios negocios y verticales.

## Refutación

Debe rechazarse o reducirse si depende totalmente de Zabal, cada cliente sigue
siendo artesanal, no mejora frente a un proceso manual o añade burocracia sin
valor.

## Conclusión

No construimos chatbots uno a uno.

Hemos creado un sistema que entiende cada negocio y genera su asistente.
