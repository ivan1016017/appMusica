export class Album {

    id: number;
    titulo: string;
    anio: number;
    descripcion: string;
    medio: Medio;
    usuario: number;
    interpretes: Array<string>;
    canciones: Array<Cancion>;
    generos: Array<string>;
    cancion_interpretes: Array<string>;
    cancion_generos: Array<any>;
    usuarios_en_album: Array<any>;
    album_original_id: number;
    es_compartido: boolean;


    constructor(
        id: number,
        titulo: string,
        anio: number,
        descripcion: string,
        medio: Medio,
        usuario: number,
        interpretes: Array<string>,
        canciones: Array<Cancion>,
        generos: Array<string>,
        cancion_interpretes:Array<string>,
        cancion_generos: Array<any>,
        usuarios_en_album: Array<any>,
        album_original_id: number,
        es_compartido: boolean

    ){
        this.id = id,
        this.titulo = titulo,
        this.anio = anio,
        this.descripcion = descripcion,
        this.medio = medio,
        this.usuario = usuario,
        this.interpretes = interpretes,
        this.canciones = canciones,
        this.generos = generos,
        this.cancion_interpretes = cancion_interpretes,
        this.cancion_generos = cancion_generos,
        this.usuarios_en_album = usuarios_en_album,
        this.album_original_id = album_original_id,
        this.es_compartido = es_compartido
    }
}

export class Medio{
    llave: string;
    valor: number

    constructor(
        llave: string,
        valor:number
    ){
        this.llave = llave,
        this.valor = valor
    }
}

export class Genero{
  llave: string;
  valor: number
  constructor(
    llave: string,
    valor: number
  ){
    this.llave = llave,
    this.valor = valor
  }
}

export class Cancion{
    id: number;
    titulo: string;
    minutos: number;
    segundos: number;
    interprete: string;

    constructor(
        id: number,
        titulo: string,
        minutos: number,
        segundos: number,
        interprete: string
    ){
        this.id = id,
        this.titulo = titulo,
        this.minutos = minutos,
        this.segundos = segundos,
        this.interprete = interprete
    }
}

export class Usuario {
  id: number;
  nombre: string;
  albumes: Array<any>;
  albumes_en_usuario: Array<any>

  constructor(
      id: number,
      nombre: string,
      albumes: Array<any>,
      albumes_en_usuario: Array<any>
  ){
      this.id = id;
      this.nombre = nombre;
      this.albumes = albumes
      this.albumes_en_usuario = albumes_en_usuario
  }
}

