// Puente Google Tasks → Claude (BELMAR)
// Copia cada hora todas tus tareas de Google Tasks a una hoja de Google Sheets
// para que Claude pueda leerlas y pasarlas a Notion.
// Requiere activar el servicio avanzado "Google Tasks API" (Servicios → +).

const NOMBRE_HOJA = 'Puente Google Tasks → Claude';

// Ejecuta esta función UNA vez: crea la hoja, programa la copia cada hora y hace la primera copia.
function configurar() {
  const props = PropertiesService.getScriptProperties();
  let id = props.getProperty('SHEET_ID');
  if (!id) {
    id = SpreadsheetApp.create(NOMBRE_HOJA).getId();
    props.setProperty('SHEET_ID', id);
  }
  ScriptApp.getProjectTriggers().forEach(t => ScriptApp.deleteTrigger(t));
  ScriptApp.newTrigger('copiarTareas').timeBased().everyHours(1).create();
  copiarTareas();
  Logger.log('Listo. Hoja: ' + SpreadsheetApp.openById(id).getUrl());
}

// Se ejecuta sola cada hora.
function copiarTareas() {
  const id = PropertiesService.getScriptProperties().getProperty('SHEET_ID');
  const hoja = SpreadsheetApp.openById(id).getSheets()[0];
  const filas = [['Lista', 'Tarea', 'Notas', 'Fecha límite', 'Estado', 'Correo de origen', 'Actualizada', 'ID']];

  let tokenListas;
  do {
    const listas = Tasks.Tasklists.list({ maxResults: 100, pageToken: tokenListas });
    (listas.items || []).forEach(lista => {
      let tokenTareas;
      do {
        const res = Tasks.Tasks.list(lista.id, { maxResults: 100, showCompleted: true, pageToken: tokenTareas });
        (res.items || []).forEach(t => {
          const correo = (t.links || []).filter(l => l.type === 'email').map(l => l.link).join(' ');
          filas.push([
            lista.title,
            t.title || '',
            t.notes || '',
            t.due ? t.due.substring(0, 10) : '',
            t.status === 'completed' ? 'Hecha' : 'Pendiente',
            correo,
            t.updated || '',
            t.id,
          ]);
        });
        tokenTareas = res.nextPageToken;
      } while (tokenTareas);
    });
    tokenListas = listas.nextPageToken;
  } while (tokenListas);

  hoja.clearContents();
  hoja.getRange(1, 1, filas.length, filas[0].length).setValues(filas);
}
