import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { Album} from '../album';
import { AlbumService } from '../album.service';
import { Usuario } from 'src/app/usuario/usuario';
import { UsuarioService } from 'src/app/usuario/usuario.service';

@Component({
  selector: 'app-album-join-user',
  templateUrl: './album-join-user.component.html',
  styleUrls: ['./album-join-user.component.css']
})
export class AlbumJoinUserComponent implements OnInit {

  userId: number;
  token: string;
  albumId: number;
  album: Album;
  albumUserForm !: FormGroup;
  users: Array<Usuario>

  constructor(
    private albumService: AlbumService,
    private usuarioService: UsuarioService,
    private formBuilder: FormBuilder,
    private router: ActivatedRoute,
    private routerPath: Router,
    private toastr: ToastrService
  ) { }

  ngOnInit() {
    if(!parseInt(this.router.snapshot.params.userId) || this.router.snapshot.params.userToken === " "){
      this.showError("No hemos podido identificarlo, por favor vuelva a iniciar sesión.")
    }
    else{
      this.userId = parseInt(this.router.snapshot.params.userId)
      this.token = this.router.snapshot.params.userToken
      this.albumId = this.router.snapshot.params.albumId
      this.albumService.getAlbum(this.token, this.albumId)
      .subscribe(album => {
        this.album = album
        this.albumUserForm = this.formBuilder.group({
          tituloAlbum: [album.titulo, [Validators.required]],
          idUsuario: ["", [Validators.required]],
          nombreUsuario: ["", [Validators.required]]
        })
        this.getUsuarios(album.usuarios_en_album)
      })
    }
  }


  getUsuarios(usuariosAlbum: Array<any>){
    let usuariosNoAgregadas: Array<Usuario> = []
    this.usuarioService.getUsuarios()
    .subscribe(usuarios => {
      usuarios.map(u => {
        if(!usuariosAlbum.includes(u.id)){
          usuariosNoAgregadas.push(u)
        }
      })
    })
    this.users = usuariosNoAgregadas
  }

  cancelarAsociacion(){
    this.albumUserForm.reset()
    this.routerPath.navigate([`/albumes/${this.userId}/${this.token}`])
  }

  asociarUsuario(){
    this.albumService.asociarUsuario(this.albumId, this.albumUserForm.get('idUsuario')?.value, this.token)
    .subscribe(usuario => {
      this.showSuccess(this.albumUserForm.get('tituloAlbum')?.value, usuario.nombre)
      this.albumUserForm.reset()
      this.routerPath.navigate([`/albumes/${this.userId}/${this.token}`])
    },
    error=> {
      if(error.statusText === "UNPROCESSABLE ENTITY"){
        this.showError("No hemos podido identificarlo, por favor vuelva a iniciar sesión.")
      }
      else{
        this.showError("Ha ocurrido un error. " + error.message)
      }
    })
  }

  onSelect(albumId: any){
    this.albumUserForm.get('idUsuario')?.setValue(albumId)
  }

  showError(error: string){
    this.toastr.error(error, "Error")
  }

  showSuccess(tituloAlbum: string, tituloNombre: string) {
    this.toastr.success(`Se agrego el album ${tituloAlbum} al usuario ${tituloNombre} `, "Asociación exitosa");
  }

}
