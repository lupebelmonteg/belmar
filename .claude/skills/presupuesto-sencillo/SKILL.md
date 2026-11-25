---
name: presupuesto-sencillo
description: Plantilla de presupuesto en PDF de una página de Lupe (estilo Digiocracy / Civitatis): cabecera "PRESUPUESTO" con el logo del cliente, secciones "Siempre incluido" e "Inversión", una fila por partida con el importe a la derecha, total, enlaces de Instagram/YouTube/LinkedIn/IMDB y el logo de BELMAR TEAM. Úsala cuando Lupe pida "hazme un presupuesto", "prepara la propuesta para…", "haz el presupuesto como el de Civitatis/Digiocracy", o un presupuesto sencillo para un cliente o evento. Para las propuestas largas, de lujo, con concepto creativo (estilo editorial azul marino) usa mejor la skill de BELMAR "belmar-presupuesto".
---

# Presupuesto sencillo de Lupe

PDF de **una sola página**, limpio, con este orden:

1. Cabecera: **PRESUPUESTO** + logo del cliente (o su nombre en texto) con línea del color de marca.
2. Título "Propuesta de cobertura para …" y subtítulo (eventos y fechas).
3. Párrafo de introducción.
4. **Siempre incluido**: lista de viñetas (qué se entrega, equipo, forma de pago…).
5. **Inversión**: una fila por partida (evento o servicio) con etiqueta, nombre, detalle y precio a la derecha con "+ IVA". Debajo, el **TOTAL**.
6. Pie: **solo enlaces** (Instagram, YouTube, LinkedIn, IMDB) y el logo pequeño de **BELMAR TEAM**. Sin teléfono ni correo (decisión de Lupe).

## Estilo (aprobado por Lupe el 25/11/2026)
- Color de acento: **#74BBB5** (el verde azulado del recuadro "Sea Light Blue" que ella enseñó; no el código #2ED9C3, que sale más vivo). Texto oscuro #2B2B2B y gris #7A7A7A.
- Tipografía Liberation Sans (parecida a Helvetica/Arial).
- Los importes van **sin IVA**, con "+ IVA" debajo.
- La marca es **BELMAR** (el logo trae "TEAM"): nunca "BELMAR Studio".

## Cómo se genera
1. Copia `ejemplos/civitatis-enero-2027.json` y cámbialo (cliente, textos, partidas, importes, total, ruta de salida).
2. Si el cliente tiene logo, ponlo en `assets/clientes/<cliente>.png` (recortado, fondo transparente o blanco) y apúntalo en `logo_cliente`. Si no, la cabecera usa el nombre del cliente en mayúsculas.
3. Ejecuta, desde esta carpeta: `python3 build_presupuesto.py mi-presupuesto.json`.
4. Mira el PDF (conviértelo a imagen para revisarlo), enséñaselo a Lupe y ajusta.

Necesita `reportlab` y la fuente Liberation Sans (paquete `fonts-liberation`). El script avisa si no caben las partidas en una página (máximo cómodo: 3 o 4).

## Reglas de Lupe para estos presupuestos
- No inventes datos: si no sabes el número de fotos, plazos de entrega o rondas de revisión, **pregunta** o déjalo fuera (el de Digiocracy llevaba "máximo 7 días hábiles, hasta dos rondas de revisión": no lo copies sin confirmar).
- Habla de **tarifas mantenidas** solo si es verdad (en Civitatis: mismas que el año pasado, que a su vez eran las del anterior; solo sube el CiviDay por tener más horas).
- El pago habitual es en dos veces: **50 % para reservar fecha y 50 % con la entrega**.
- Nunca envíes el correo con el presupuesto: **prepara un borrador de Gmail** con el PDF adjunto (créalo con la ruta del archivo en el adjunto) y avisa de que lo compruebe y lo envíe ella. Su firma de Gmail lleva el teléfono: avísala por si no lo quiere.
- Si hay que cambiar el PDF después de crear el borrador, crea un borrador nuevo con el PDF nuevo y borra el anterior.

## Ejemplo guardado
`ejemplos/civitatis-enero-2027.json`: Kick-off 700 €, CiviDay 1.350 €, FITUR 1.900 € (una jornada completa y otra de media jornada de refuerzo), total 3.950 € + IVA.
