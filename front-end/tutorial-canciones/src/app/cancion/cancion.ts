import { Usuario } from '../album/album';
export class Cancion {
    id: number;
    titulo: string;
    minutos: number;
    segundos: number;
    interprete: string;
    albumes: Array<any>;
    genero: Genero;
    es_favorita: boolean;
    es_compartida:boolean;
    id_original:number;
    usuarios_compartidos: Array<any>;
    usuario:number;

    constructor(
        id: number,
        titulo: string,
        minutos: number,
        segundos: number,
        interprete: string,
        albumes: Array<any>,
        es_favorita: boolean,
        genero: Genero,
        usuarios_compartidos: Array<any>,
        es_compartida:boolean,
        id_original:number,
        usuario:number

    ){
        this.id = id
        this.titulo = titulo
        this.minutos = minutos
        this.segundos = segundos
        this.interprete = interprete
        this.es_favorita = es_favorita
        this.albumes = albumes
        this.genero = genero
        this.usuarios_compartidos = usuarios_compartidos
        this.es_compartida = es_compartida
        this.id_original = id_original
        this.usuario = usuario
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
