export class Usuario {
    id: number;
    nombre: string;
    albumes: Array<any>;
    albumes_en_usuario: Array<any>
    canciones_compartidas:Array<any>

    constructor(
        id: number,
        nombre: string,
        albumes: Array<any>,
        albumes_en_usuario: Array<any>,
        canciones_compartidas:Array<any>
    ){
        this.id = id;
        this.nombre = nombre;
        this.albumes = albumes;
        this.albumes_en_usuario = albumes_en_usuario;
        this.canciones_compartidas = canciones_compartidas
    }
}
