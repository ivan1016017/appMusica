import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Cancion } from './cancion';
import { Album } from '../album/album';
import { Comentario } from './comment'
import { Usuario } from '../usuario/usuario';

@Injectable({
  providedIn: 'root'
})

export class CancionService {



  private backUrl: string = "http://localhost:5000"

  constructor(private http: HttpClient) { }

  getCancionesAlbum(idAlbum: number, token: string): Observable<Cancion[]>{
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    })
    return this.http.get<Cancion[]>(`${this.backUrl}/album/${idAlbum}/canciones`, {headers: headers})
  }

  getCanciones(usuario: number, token: string): Observable<Cancion[]>{
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    })
    return this.http.get<Cancion[]>(`${this.backUrl}/usuario/${usuario}/canciones`, { headers })
  }

  getAlbumesCancion(token: string, cancionId: number): Observable<Album[]>{
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    })

    return this.http.get<Album[]>(`${this.backUrl}/cancion/${cancionId}/albumes`, {headers})
  }

  crearCancion(idUsuario: number, token: string, cancion: Cancion):Observable<Cancion>{
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    })

    return this.http.post<Cancion>(`${this.backUrl}/usuario/${idUsuario}/canciones`, cancion, {headers: headers})
  }

  getCancion(token: string, cancionId: number): Observable<Cancion>{
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    })

    return this.http.get<Cancion>(`${this.backUrl}/cancion/${cancionId}`, {headers})
  }

  editarCancion(token: string, cancion: Cancion, cancionId: number):Observable<Cancion>{
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    })

    return this.http.put<Cancion>(`${this.backUrl}/cancion/${cancionId}`, cancion, {headers})
  }

  eliminarCancion(token: string, cancionId: number): Observable<Cancion>{
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    })

    return this.http.delete<Cancion>(`${this.backUrl}/cancion/${cancionId}`, {headers})
  }

  changeFavoriteState(token: string, cancionId: number):Observable<Cancion>{
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    })

    return this.http.put<Cancion>(`${this.backUrl}/cancion/${cancionId}/change_favorite_state`, {}, {headers})
  }

  asociarUsuario(cancionId: number, user_sharedId:number, idUsuario: number, token: string  ):Observable<Usuario>{
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    })
    return this.http.post<Usuario>(`${this.backUrl}/usuario/${idUsuario}/canciones/song_shared`,  {"id_cancion":cancionId, "id_shared_user":user_sharedId},  {headers: headers})
  }
  crearComentario(cancionId: number, token: string, comentario: Comentario):Observable<Comentario>{
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    })

    return this.http.post<Comentario>(`${this.backUrl}/cancion/${cancionId}/comentarios`, comentario, {headers: headers})
    }

  getComentarios(token: string, cancionId: number): Observable<Comentario[]>{
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    })

    return this.http.get<Comentario[]>(`${this.backUrl}/cancion/${cancionId}/comentarios`, {headers})
    }

  getUsuario(idUsuario: number, token: string): Observable<Usuario>{
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    })
    return this.http.get<Usuario>(`${this.backUrl}/usuario/${idUsuario}`, {headers})
  }

}


