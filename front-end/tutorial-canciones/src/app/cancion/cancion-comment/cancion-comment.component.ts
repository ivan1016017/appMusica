import { Component, OnInit, Input } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ToastrService } from 'ngx-toastr';
import { ActivatedRoute, Router } from '@angular/router';
import { Comentario } from '../comment'
import { CancionService } from '../cancion.service';
import { Cancion } from '../cancion';
import { Usuario } from 'src/app/usuario/usuario';

@Component({
  selector: 'app-cancion-comment',
  templateUrl: './cancion-comment.component.html',
  styleUrls: ['./cancion-comment.component.css']
})
export class CancionCommentComponent implements OnInit {

  @Input() cancionId: number;
  deshabilitar = false
  userId: number
  token: string
  commentForm: FormGroup
  comments: Array<any>;
  creada: string
  dateTime: Date
  user: Usuario
  comment: Comentario

  constructor(
    private cancionService: CancionService,
    private formBuilder: FormBuilder,
    private router: ActivatedRoute,
    private routerPath: Router,
    private toastr: ToastrService
    ) { }

  ngOnChanges() {
    console.log(this.comments)
    this.getComentarios()
  }

  ngOnInit() {
      if(!parseInt(this.router.snapshot.params.userId) || this.router.snapshot.params.userToken === " "){
        this.showError("No hemos podido identificarlo, por favor vuelva a iniciar sesión.")
      }
      else{
      this.userId = parseInt(this.router.snapshot.params.userId)
      this.token = this.router.snapshot.params.userToken
      this.dateTime = new Date
      this.creada = this.dateTime.getFullYear()+'/'+(this.dateTime.getMonth()+1)+'/'+this.dateTime.getDate();
      this.getComentarios();
      this.getUser();
      this.commentForm = this.formBuilder.group({
        content: ["", [Validators.required, Validators.maxLength(1000)]],
        creada: this.creada,
        usuario: this.userId
      })

    }
  }

  habilitarComentarios() {
    this.deshabilitar = !this.deshabilitar;
  }

  crearComentario(newComentario: Comentario){
    this.cancionService.crearComentario(this.cancionId, this.token, newComentario)
    .subscribe(comentario =>{
      this.showSuccess(comentario)
      this.commentForm.reset()
      this.routerPath.navigate([`/canciones/${this.cancionId}/${this.token}`])
      this.getComentarios()
    },
    error=> {
    if(error.statusText === "UNAUTHORIZED"){
      this.showWarning("Su sesión ha caducado, por favor vuelva a iniciar sesión.")
    }
    else if(error.statusText === "UNPROCESSABLE ENTITY"){
      this.showError("No hemos podido identificarlo, por favor vuelva a iniciar sesión.")
    }
    else{
      this.showError("Ha ocurrido un error. " + error.message)
    }
    })
  }



  cancelarComentario(){
    this.commentForm.reset();
    this.deshabilitar = false;
    this.routerPath.navigate([`/canciones/${this.userId}/${this.token}`])
  }

  showError(error: string){
    this.toastr.error(error, "Error")
  }

  showWarning(warning: string){
    this.toastr.warning(warning, "Error de autenticación")
  }

  showSuccess(comentario: Comentario) {
    this.toastr.success("Su comentario fue creado");
  }

  getComentarios():void{
    this.cancionService.getComentarios(this.token, this.cancionId)
    .subscribe(comentarios=> {
      this.comments = comentarios
      })
  }

  getUser(): void{
    this.cancionService.getUsuario(this.userId, this.token)
      .subscribe(user=> {
    this.user = user
    })
  }

}
