from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from datetime import datetime
import enum


db = SQLAlchemy()

albumes_canciones = db.Table('album_cancion',
    db.Column('album_id', db.Integer, db.ForeignKey('album.id'), primary_key = True),
    db.Column('cancion_id', db.Integer, db.ForeignKey('cancion.id'), primary_key = True))

albumes_usuarios = db.Table('album_usuario',
    db.Column('album_id', db.Integer, db.ForeignKey('album.id'), primary_key = True),
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuario.id'), primary_key = True))

canciones_usuarios = db.Table('cancion_usuario',
    db.Column('cancion_id', db.Integer, db.ForeignKey('cancion.id'), primary_key = True),
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuario.id'), primary_key = True))

class Medio(enum.Enum):
   DISCO = 1
   CASETE = 2
   CD = 3

class Genero(enum.Enum):
   BACHATA = 1
   BALADAS = 2
   BANDA = 3
   BLUES = 4
   BOLERO = 5

class Cancion(db.Model):
    __tablename__ = 'cancion'
    id = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String(128))
    minutos = db.Column(db.Integer)
    segundos = db.Column(db.Integer)
    es_favorita = db.Column(db.Boolean, default = False)
    es_compartida = db.Column(db.Boolean, default = False)
    id_original=db.Column(db.Integer)
    interprete = db.Column(db.String(128))
    genero = db.Column(db.Enum(Genero))
    usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    albumes = db.relationship('Album', secondary = 'album_cancion', back_populates="canciones")
    usuarios_compartidos = db.relationship('Usuario',secondary='cancion_usuario',back_populates="canciones_compartidas")
    # comentarios = db.relationship('Comentario', backref='cancion', lazy=True)
    comentarios = db.relationship('Comentario', cascade='all, delete, delete-orphan')

    def get_shared_users(self):
        result = map(lambda c: c.id, self.usuarios_compartidos)
        return list(result)

class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(128))
    anio = db.Column(db.Integer)
    descripcion = db.Column(db.String(512))
    medio = db.Column(db.Enum(Medio))
    usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    album_original_id = db.Column(db.Integer)
    es_compartido = db.Column(db.Boolean, default = False)
    canciones = db.relationship('Cancion', secondary = 'album_cancion', back_populates="albumes")
    usuarios_en_album = db.relationship('Usuario', secondary = 'album_usuario', back_populates="albumes_en_usuario")
    def cancion_interpretes(self):
        result = map(lambda c: c.interprete, self.canciones)
        return list(result)
    def cancion_generos(self):
        result = map(lambda c: c.titulo, self.canciones)
        return list(result)
    
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    contrasena = db.Column(db.String(50))
    albumes = db.relationship('Album', cascade='all, delete, delete-orphan')
    canciones = db.relationship('Cancion', cascade='all, delete, delete-orphan')
    canciones_compartidas = db.relationship('Cancion', secondary='cancion_usuario', back_populates="usuarios_compartidos")
    # comentarios = db.relationship('Comentario', cascade='all, delete, delete-orphan')
    albumes_en_usuario = db.relationship('Album', secondary = 'album_usuario', back_populates="usuarios_en_album")
    def id_canciones_compartidas(self):
        result = map(lambda c: c.id, self.canciones_compartidas)
        return list(result)
class Comentario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    creada = db.Column(db.String(10))
    cancion_id = db.Column(db.Integer, db.ForeignKey("cancion.id"))
    usuario = db.Column(db.Integer)


class EnumADiccionario(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return {"llave": value.name, "valor": value.value}

class CancionSchema(SQLAlchemyAutoSchema):
    genero = EnumADiccionario(attribute=("genero"))
    class Meta:
         model = Cancion
         include_relationships = True
         load_instance = True

class AlbumSchema(SQLAlchemyAutoSchema):
    medio = EnumADiccionario(attribute=("medio"))
    cancion_interpretes = fields.Function(lambda obj: obj.cancion_interpretes())
    cancion_generos = fields.Function(lambda obj: obj.cancion_generos())
    class Meta:
         model = Album
         include_relationships = True
         load_instance = True

class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = Usuario
         include_relationships = True
         load_instance = True

class ComentarioSchema(SQLAlchemyAutoSchema):
    class Meta:
         model = Comentario
         include_relationships = True
         load_instance = True
