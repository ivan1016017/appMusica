import { Comentario } from './comment'

let dateTime = new Date()
let NoTimeDate = dateTime.getFullYear()+'/'+(dateTime.getMonth()+1)+'/'+dateTime.getDate();

export const COMMENTS: Comentario[] = [
  // { id: 11, content: 'Primer comentario de prueba', usuario: 1},
  // { id: 12, content: 'Segundo comentario de prueba', usuario: 1 },
  // { id: 13, content: 'Tercer comentario de prueba', usuario: 1 }
  { id: 11, content: 'Primer comentario de prueba', cancion: 1},
  { id: 12, content: 'Segundo comentario de prueba', cancion: 1 },
  { id: 13, content: 'Tercer comentario de prueba', cancion: 1 }
];
