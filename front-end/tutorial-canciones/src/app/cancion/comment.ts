export class Comentario {
  id: number;
  content: string;
  creada: string;
  cancion: number;
  usuario: number;


  constructor(
    id: number,
    content: string,
    creada: string,
    cancion: number,
    usuario: number
  ){
      this.id=id;
      this.content = content;
      this.creada=creada;
      this.cancion = cancion;
      this.usuario = usuario;
    }
}
