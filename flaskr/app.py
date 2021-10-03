from .vistas import VistaUsuarioCanciones
from flaskr import create_app
from flask_restful import Api
from .modelos import db, Cancion, Usuario, Album, Comentario
from .vistas import VistaCanciones, VistaCancion, VistaSignIn, VistaAlbum, VistaAlbumsUsuario, VistaCancionesAlbum, VistaLogIn, VistaAlbumesCanciones, VistaCancionCambiarFavorito, VistaUsuarioAlbum, VistaUsuario, VistaUsuarios, VistaComentario, VistaCancionByid
from flask_jwt_extended import JWTManager
from flask_cors import CORS, cross_origin

app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()
cors = CORS(app)

api = Api(app)
api.add_resource(VistaCanciones, '/usuario/<int:id_usuario>/canciones')
api.add_resource(VistaCancion, '/cancion/<int:id_cancion>')
api.add_resource(VistaCancionCambiarFavorito, '/cancion/<int:id_cancion>/change_favorite_state')
api.add_resource(VistaAlbumesCanciones, '/cancion/<int:id_cancion>/albumes')
api.add_resource(VistaSignIn, '/signin')
api.add_resource(VistaLogIn, '/logIn')
api.add_resource(VistaAlbumsUsuario, '/usuario/<int:id_usuario>/albumes')
api.add_resource(VistaAlbum, '/album/<int:id_album>')
api.add_resource(VistaCancionesAlbum, '/album/<int:id_album>/canciones')
api.add_resource(VistaUsuarioAlbum, '/usuario/<int:id_usuario>/albumes/change_shared_state')
api.add_resource(VistaUsuario, '/usuario/<int:id_usuario>')
api.add_resource(VistaUsuarios, '/usuarios')
api.add_resource(VistaUsuarioCanciones,'/usuario/<int:id_usuario>/canciones/song_shared')
api.add_resource(VistaComentario, '/cancion/<int:id_cancion>/comentarios')
api.add_resource(VistaCancionByid, '/cancion/byId/<int:id_cancion>')

jwt = JWTManager(app)
