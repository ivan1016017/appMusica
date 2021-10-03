import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { Usuario } from 'src/app/usuario/usuario';
import { UsuarioService } from 'src/app/usuario/usuario.service';
import { Cancion } from '../cancion';
import { CancionService } from '../cancion.service';

@Component({
  selector: 'app-cancion-join-user',
  templateUrl: './cancion-join-user.component.html',
  styleUrls: ['./cancion-join-user.component.css']
})
export class CancionJoinUserComponent implements OnInit {

  userId: number;
  token: string;
  cancionId: number;
  cancion: Cancion;
  cancionUserForm !: FormGroup;
  users: Array<Usuario>

  constructor(
    private cancionService: CancionService,
    private usuarioService: UsuarioService,
    private formBuilder: FormBuilder,
    private router: ActivatedRoute,
    private routerPath: Router,
    private toastr: ToastrService
  ) { }

  ngOnInit(): void {
    if(!parseInt(this.router.snapshot.params.userId) || this.router.snapshot.params.userToken === " "){
      this.showError("No hemos podido identificarlo, por favor vuelva a iniciar sesión.")
    }
    else{
      this.userId = parseInt(this.router.snapshot.params.userId)
      this.token = this.router.snapshot.params.userToken
      this.cancionId = this.router.snapshot.params.cancionId
      this.cancionService.getCancion(this.token, this.cancionId)
      .subscribe(cancion => {
        this.cancion = cancion
        this.cancionUserForm = this.formBuilder.group({
          tituloCancion: [cancion.titulo, [Validators.required]],
          idUsuario: ["", [Validators.required]],
          nombreUsuario: ["", [Validators.required]]
        })
        this.getUsuarios(cancion.usuarios_compartidos)
      })
    }
  }

  getUsuarios(usuariosCancion: Array<any>){
    let usuariosPorAgregar: Array<Usuario> = []
    this.usuarioService.getUsuarios()
    .subscribe(usuarios => {
      usuarios.map(u => {
        if(!usuariosCancion.includes(u.id) && u.id!=this.userId ){
          usuariosPorAgregar.push(u)}
      })
    })
    this.users = usuariosPorAgregar
  }

  cancelarAsociacion(){
    this.cancionUserForm.reset()
    this.routerPath.navigate([`/canciones/${this.userId}/${this.token}`])
  }

  asociarUsuario() {
    this.cancionService.asociarUsuario(this.cancionId, this.cancionUserForm.get('idUsuario')?.value, this.userId, this.token)
    .subscribe(usuario => {
      this.showSuccess(this.cancionUserForm.get('tituloCancion')?.value, this.cancionUserForm.get('nombreUsuario')?.value)
      this.cancionUserForm.reset()
      this.routerPath.navigate([`/canciones/${this.userId}/${this.token}`])
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
  showSuccess(tituloCancion: string, usuarioNombre: string) {
    this.toastr.success(`Se agrego la cancion ${tituloCancion} al usuario ${usuarioNombre} `, "Asociación exitosa")
  }

  onSelect(cancionId: any){
    this.cancionUserForm.get('idUsuario')?.setValue(cancionId)
  }


  showError(error: string) {
    this.toastr.error(error, "Error");
  }

}
