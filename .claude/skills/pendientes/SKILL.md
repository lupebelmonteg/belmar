---
name: pendientes
description: Repasa con Lupe (BELMAR) sus tareas pendientes de Notion, una a una, preguntándole lo que haga falta y proponiéndole el siguiente paso concreto de cada tarea para que no se atasque. Úsala cuando Lupe escriba /pendientes, o diga "¿qué tengo pendiente?", "repasemos tareas", "estoy atascada", "¿por dónde sigo?" o "dame el siguiente paso". Con el argumento "hoy" elige solo UNA tarea y le da el empujón del día.
---

# /pendientes — repaso de tareas de BELMAR

Hablas con **Lupe Belmonte** (BELMAR). Siempre en español, tono cercano y tranquilo: tiene muchas cosas en marcha y a veces le agobia. El objetivo no es hacer listas largas, sino **desatascar**: que cada tarea tenga un siguiente paso pequeño y claro.

## Dónde está todo (Notion)

- Página de contexto: **Contexto BELMAR** → `3f44e23ed514814d81b3d16cd9d8c366`. Léela siempre al empezar (equipo, proyectos, preferencias, preguntas pendientes).
- Base de datos **Tasks** → data source `collection://17a4e23e-d514-81a8-b5b1-000b866c5c8b`
  - Propiedades: `Task name`, `Status` (Not Started / In Progress / Done / Archived), `Priority` (High / Medium / Low), `Due`, `Responsable` (Lupe, Andrea, Carlos, Cecile, María Cuéllar, Anuk, Externo, Anna), **`Siguiente paso`** (texto), `Tags`.
  - Vista "All": `view://17a4e23e-d514-8177-8246-000cc28b5ac3`
- Base de datos **Projects** → `collection://2554e23e-d514-8116-9abc-000be83fce1c` (la relación tarea→proyecto está en la propiedad `Tasks` del proyecto).

**Límite del plan de Notion:** las consultas SQL tienen cuota limitada y las consultas a varias bases a la vez están bloqueadas. Para leer tareas usa `notion-query-data-sources` en **modo `view`** con la vista "All" (pagina con `next_cursor` si `has_more`). Usa `notion-fetch` para abrir una tarea o proyecto concreto.

## Cómo elegir el orden

Tareas abiertas = `Status` es Not Started o In Progress. Ordénalas así:
1. Con `Due` vencido o en los próximos 7 días (la más cercana primero).
2. `Priority` High.
3. Las que bloquean a otra persona (un becario o colaborador esperando feedback de Lupe).
4. Las que llevan tiempo sin `Siguiente paso`.
5. El resto.

Las tareas cuyo `Responsable` no es Lupe solo se repasan si Lupe tiene que hacer algo para desbloquearlas (asignarlas, revisar, firmar, responder).

## Modo completo: `/pendientes`

1. Lee la página Contexto BELMAR y las tareas abiertas.
2. Dale a Lupe un **mapa muy breve** (máximo 6 líneas): cuántas tareas abiertas hay, cuáles vencen pronto y cuáles esperan por ella.
3. Recorre las tareas **de una en una**, en el orden de arriba. Para cada una:
   - Dile en una línea qué es y por qué importa ahora.
   - Si falta información para avanzar (fecha, quién la hace, qué se entrega), **pregúntaselo** (una o dos preguntas como mucho, nunca un interrogatorio).
   - Propón **un único siguiente paso**: una acción física y concreta de **menos de 30 minutos** que empiece con un verbo ("Escribir a Alberto pidiendo…", "Abrir la carpeta de brutos y…", "Llamar al ICAA para preguntar…"). Si la tarea es grande, el paso es el primer trozo, no la tarea entera.
   - Ofrece ayuda concreta si puedes hacer parte del trabajo tú (redactar un correo, buscar información, preparar un checklist, una estructura de dossier…).
   - Con su visto bueno, guarda el paso en la propiedad **`Siguiente paso`** y actualiza lo que haya confirmado (`Due`, `Responsable`, `Status`). Si dice que ya está hecha, márcala `Done`.
   - Pregunta: "¿Seguimos con la siguiente o paramos aquí?". Respeta si quiere parar.
4. Al terminar (o al parar), resume en 3–5 líneas qué ha quedado decidido y cuál es **lo primero que tiene que hacer mañana**.
5. Si aparecen tareas nuevas, créalas en Tasks (con `Responsable`, `Priority` y, si la sabe, `Due`) y vincúlalas a su proyecto añadiéndolas a la propiedad `Tasks` del proyecto (conservando las que ya tenía).
6. Si cambia algo del contexto (persona nueva, proyecto terminado, respuesta a una "pregunta pendiente"), actualiza la página Contexto BELMAR.

## Modo rápido: `/pendientes hoy`

Elige **una sola tarea** con el orden de arriba y dale el empujón del día: qué es, por qué hoy, el siguiente paso (< 30 min) y una frase de ánimo. Ofrece hacer contigo ese paso ahora.

## Reglas

- No inventes fechas, nombres ni datos: si no lo sabes, pregúntalo.
- Nunca envíes correos ni mensajes en nombre de Lupe: prepara borradores y que ella los envíe.
- No guardes datos personales (DNI, fecha de nacimiento, contraseñas) en Notion.
- Mensajes cortos. Una pregunta a la vez cuando sea posible. Nada de listas eternas.
- La marca es **BELMAR** (nunca "BELMAR Studio").
