from flask import request
from ..modelos import db, Cancion, CancionSchema, Usuario, UsuarioSchema, Album, AlbumSchema, Comentario, ComentarioSchema
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

cancion_schema = CancionSchema()
usuario_schema = UsuarioSchema()
album_schema = AlbumSchema()
comentario_schema = ComentarioSchema()

class VistaCanciones(Resource):
    @jwt_required()
    def post(self, id_usuario):
        nueva_cancion = Cancion(
                titulo=request.json["titulo"],
                minutos=request.json["minutos"],
                segundos=request.json["segundos"],
                interprete=request.json["interprete"],
                genero=request.json["genero"]
                )

        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.canciones.append(nueva_cancion)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return 'El usuario ya tiene una cancion con dicho nombre',409

        return cancion_schema.dump(nueva_cancion)

    @jwt_required()
    def get(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        return [cancion_schema.dump(al) for al in usuario.canciones]

   


class VistaCancion(Resource):

    @jwt_required()
    def get(self, id_cancion):
        usuario = Usuario.query.get_or_404(get_jwt_identity())
        cancion = Cancion.query.get_or_404(id_cancion)
        if(cancion.usuario == usuario.id):
            return cancion_schema.dump(cancion)
        else:
            return '', 401

    @jwt_required()
    def put(self, id_cancion):
        usuario = Usuario.query.get_or_404(get_jwt_identity())
        cancion = Cancion.query.get_or_404(id_cancion)
        if(cancion.usuario == usuario.id):
            cancion.titulo = request.json.get("titulo",cancion.titulo)
            cancion.minutos = request.json.get("minutos",cancion.minutos)
            cancion.segundos = request.json.get("segundos",cancion.segundos)
            cancion.interprete = request.json.get("interprete",cancion.interprete)
            cancion.genero = request.json.get("genero",cancion.genero)
            db.session.commit()
            return cancion_schema.dump(cancion)
        else:
            return '', 401

    @jwt_required()
    def delete(self, id_cancion):
        usuario = Usuario.query.get_or_404(get_jwt_identity())
        cancion = Cancion.query.get_or_404(id_cancion)
        if(cancion.usuario == usuario.id):
            db.session.delete(cancion)
            db.session.commit()
            return '',204
        else: 
            return '', 401

class VistaCancionCambiarFavorito(Resource):
    @jwt_required()
    def put(self, id_cancion):
        usuario = Usuario.query.get_or_404(get_jwt_identity())
        cancion = Cancion.query.get_or_404(id_cancion)
        if(cancion.usuario == usuario.id):
            cancion.es_favorita = not cancion.es_favorita
            db.session.commit()
            return cancion_schema.dump(cancion)
        else: 
            return '', 401
 
class VistaAlbumesCanciones(Resource):
    @jwt_required()
    def get(self, id_cancion):
        usuario = Usuario.query.get_or_404(get_jwt_identity())
        cancion = Cancion.query.get_or_404(id_cancion)
        if(cancion.usuario == usuario.id):
            return [album_schema.dump(al) for al in cancion.albumes]
        else:
            return '', 401

class VistaAlbumsUsuario(Resource):
    @jwt_required()
    def post(self, id_usuario):
        nuevo_album = Album(titulo=request.json["titulo"], anio=request.json["anio"], descripcion=request.json["descripcion"], medio=request.json["medio"])
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.albumes.append(nuevo_album)
        usuario.albumes_en_usuario.append(nuevo_album)
        nuevo_album.usuarios_en_album.append(usuario)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return 'El usuario ya tiene un album con dicho nombre',409

        return album_schema.dump(nuevo_album)

    @jwt_required()
    def get(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        return [album_schema.dump(al) for al in usuario.albumes]

class VistaCancionesAlbum(Resource):
    @jwt_required()
    def post(self, id_album):
        usuario = Usuario.query.get_or_404(get_jwt_identity())
        album = Album.query.get_or_404(id_album)
        
        if(album.usuario == usuario.id):
            if "id_cancion" in request.json.keys():
                
                nueva_cancion = Cancion.query.get(request.json["id_cancion"])
                if nueva_cancion is not None:
                    album.canciones.append(nueva_cancion)
                    db.session.commit()
                else:
                    return 'Canción errónea',404
            else: 
                nueva_cancion = Cancion(titulo=request.json["titulo"], minutos=request.json["minutos"], segundos=request.json["segundos"], interprete=request.json["interprete"], genero=request.json["genero"])
                album.canciones.append(nueva_cancion)
            db.session.commit()
            return cancion_schema.dump(nueva_cancion)
        else:
            return '', 401
       
    @jwt_required()
    def get(self, id_album):
        usuario = Usuario.query.get_or_404(get_jwt_identity())
        album = Album.query.get_or_404(id_album)
        if(album.usuario == usuario.id):
            return [cancion_schema.dump(ca) for ca in album.canciones]
        else:
            return '', 401

class VistaAlbum(Resource):
    @jwt_required()
    def get(self, id_album):
        usuario = Usuario.query.get_or_404(get_jwt_identity())
        album = Album.query.get_or_404(id_album)
        if(album.usuario == usuario.id):
            return album_schema.dump(album)
        else:
            return '', 401

    @jwt_required()
    def put(self, id_album):
        usuario = Usuario.query.get_or_404(get_jwt_identity())
        album = Album.query.get_or_404(id_album)
        if(album.usuario == usuario.id):
            album.titulo = request.json.get("titulo",album.titulo)
            album.anio = request.json.get("anio", album.anio)
            album.descripcion = request.json.get("descripcion", album.descripcion)
            album.medio = request.json.get("medio", album.medio)
            db.session.commit()
            return album_schema.dump(album)
        else:
            return '', 401

    @jwt_required()
    def delete(self, id_album):
        usuario = Usuario.query.get_or_404(get_jwt_identity())
        album = Album.query.get_or_404(id_album)
        if(album.usuario == usuario.id):
            db.session.delete(album)
            db.session.commit()
            return '',204
        else:
            return '', 401

class VistaUsuarioAlbum(Resource):

    def post(self, id_usuario):

        album_a_compartir = Album.query.get(request.json["id_album"])
        usuario_a_compartir = Usuario.query.get_or_404(id_usuario)
        usuario_original = Usuario.query.get_or_404(album_a_compartir.usuario)
        
        nuevo_album = Album(
        titulo = album_a_compartir.titulo,
        anio = album_a_compartir.anio,
        descripcion = album_a_compartir.descripcion,
        medio = album_a_compartir.medio,
        usuario = usuario_a_compartir.id,
        album_original_id = album_a_compartir.id,
        es_compartido = True
        )

        usuario_a_compartir.albumes.append(nuevo_album)
        album_a_compartir.usuarios_en_album.append(usuario_a_compartir)
        nuevo_album.usuarios_en_album.append(usuario_a_compartir)
        nuevo_album.usuarios_en_album.append(usuario_original)
        db.session.commit()
        return album_schema.dump(nuevo_album)
        
        # if "id_album" in request.json.keys():
            
        #     nuevo_album = Album.query.get(request.json["id_album"])
        #     if nuevo_album is not None:
        #         nuevo_album.es_compartido = True
        #         usuario.albumes.append(nuevo_album)
        #         usuario.albumes_en_usuario.append(nuevo_album)
        #         db.session.commit()
        #     else:
        #         return 'Álbum erróneo',404
        # else: 
        #     nuevo_album = Album(titulo=request.json["titulo"], anio=request.json["anio"], descripcion=request.json["descripcion"], medio=request.json["medio"])
        #     usuario.albumes.append(nuevo_album)
        # db.session.commit()
        # return album_schema.dump(nuevo_album)

class VistaUsuarioCanciones(Resource):
    def post(self, id_usuario):
        id_cancion= request.json["id_cancion"]
        cancion_compartida=Cancion.query.get_or_404(id_cancion) 
        shared_user = Usuario.query.get_or_404(request.json["id_shared_user"])

        if cancion_compartida.es_compartida:
            id_cancion_original=Cancion.query.get_or_404(cancion_compartida.id_original)
            if id_cancion_original.usuario == shared_user.id:
                 return   f'No se puede recompartir una cancion, El usuario {shared_user.id} es el dueño original de esta cancion'
       
        if cancion_compartida.usuario != id_usuario:
            return f'Cancion {id_cancion} no pertenece al usuario {id_usuario}',404
        
        if cancion_compartida.usuario == shared_user.id:
            return f'No se puede compartir la cancion {id_cancion} con el mismo usuario {shared_user.id}',404
        
        if  cancion_compartida.id in shared_user.id_canciones_compartidas():
            return f'La cancion ya esta compartida al usuario'
        
        if cancion_compartida is not None:
            shared_user.canciones_compartidas.append(cancion_compartida)
            cancion_compartida.usuarios_compartidos.append(shared_user)
            self.create_copy_cancion(cancion_compartida,shared_user)
            db.session.commit()
        else:
            return 'Cancion errónea',404
        return cancion_schema.dump(cancion_compartida)

    def create_copy_cancion(self,original_song,shared_user):
        copy_cancion = Cancion(
                titulo=original_song.titulo,
                minutos=original_song.minutos,
                segundos=original_song.segundos,
                interprete=original_song.interprete,
                genero=original_song.genero,    
                es_compartida=True,
                id_original=original_song.id
        )
        if original_song.es_compartida:
            copy_cancion.id_original=original_song.id_original
        shared_user.canciones.append(copy_cancion)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return 'El usuario ya tiene una cancion con dicho nombre',409
        return cancion_schema.dump(copy_cancion)

class VistaCancionByid(Resource):

    def get(self, id_cancion):
        return cancion_schema.dump(Cancion.query.get_or_404(id_cancion) )
class VistaUsuario(Resource):

    def get(self, id_usuario):
        return usuario_schema.dump(Usuario.query.get_or_404(id_usuario))

class VistaUsuarios(Resource):

    def get(self):
        return [usuario_schema.dump(usu) for usu in Usuario.query.all()]
 

class VistaSignIn(Resource):
    
    def post(self):
        nuevo_usuario = Usuario(nombre=request.json["nombre"], contrasena=request.json["contrasena"])
        db.session.add(nuevo_usuario)
        db.session.commit()
        token_de_acceso = create_access_token(identity = nuevo_usuario.id)
        return {"mensaje":"usuario creado exitosamente", "token":token_de_acceso}


    def put(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.contrasena = request.json.get("contrasena",usuario.contrasena)
        db.session.commit()
        return usuario_schema.dump(usuario)

    def delete(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        db.session.delete(usuario)
        db.session.commit()
        return '',204

class VistaLogIn(Resource):

    def post(self):
        usuario = Usuario.query.filter(Usuario.nombre == request.json["nombre"], Usuario.contrasena == request.json["contrasena"]).first()
        db.session.commit()
        if usuario is None:
            return "El usuario no existe", 404
        else:
            token_de_acceso = create_access_token(identity = usuario.id)
            return {"mensaje":"Inicio de sesión exitoso", "token": token_de_acceso}
   
class VistaComentario(Resource):
    @jwt_required()
    def post(self, id_cancion):
        nuevo_comentario = Comentario(
                content=request.json["content"],
                creada=request.json["creada"],
                usuario=request.json["usuario"]
                )
        cancion = Cancion.query.get_or_404(id_cancion)
        if cancion.es_compartida:
            cancion = Cancion.query.get_or_404(cancion.id_original)

        cancion.comentarios.append(nuevo_comentario)
        # usuario = Usuario.query.get_or_404(id_usuario)
        db.session.commit()

        return comentario_schema.dump(nuevo_comentario)

    @jwt_required()
    def get(self, id_cancion):
        usuario = Usuario.query.get_or_404(get_jwt_identity())
        cancion = Cancion.query.get_or_404(id_cancion)
        if cancion.es_compartida:
            cancion = Cancion.query.get_or_404(cancion.id_original)
        return [comentario_schema.dump(co) for co in cancion.comentarios]