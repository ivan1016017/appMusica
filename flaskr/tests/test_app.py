import os
import tempfile

import pytest
from flask import json

from ..app import app, db, Cancion, Usuario, Album, Comentario

@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            db.init_app(app)
            db.create_all()
        yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])

@pytest.fixture
def sign_in(client):
    nuevo_usuario = Usuario(
            nombre='test_user',
            contrasena='test_user'
            )
    db.session.add(nuevo_usuario)
    db.session.commit()
    response = client.post(
            '/logIn',
            data=json.dumps({"nombre": nuevo_usuario.nombre, "contrasena": nuevo_usuario.contrasena}),
            headers={"Content-Type": "application/json"},
            )
    json_data = json.loads(response.data)
    return {"user": nuevo_usuario, "token": json_data["token"]}


def test_cancion_a_favorito(client, sign_in):
    sign_in_data = sign_in
    user = sign_in_data["user"]
    headers = {
            "Authorization": "Bearer {}".format(sign_in_data["token"]),
            "Content-Type": "application/json"
            }

    nueva_cancion = Cancion(
            titulo="test",
            minutos="10",
            segundos="30",
            interprete="Test interprete",
            es_favorita=False,
            genero="BALADAS",
            usuario=user.id
            )
    db.session.add(nueva_cancion)
    db.session.commit()

    rv = client.put('/cancion/'+str(nueva_cancion.id)+'/change_favorite_state', headers=headers)
    json_data = json.loads(rv.data)
    assert json_data['es_favorita'] ==  True

    Cancion.query.delete()
    Usuario.query.delete()
    db.session.commit()

def test_quitar_favorito_a_cancion(client, sign_in):
    sign_in_data = sign_in
    user = sign_in_data["user"]
    headers = {
            "Authorization": "Bearer {}".format(sign_in_data["token"]),
            "Content-Type": "application/json"
            }

    nueva_cancion = Cancion(
            titulo="test",
            minutos="10",
            segundos="30",
            interprete="Test interprete",
            es_favorita=True,
            genero="BALADAS",
            usuario=user.id
            )
    db.session.add(nueva_cancion)
    db.session.commit()

    rv = client.put('/cancion/'+str(nueva_cancion.id)+'/change_favorite_state', headers=headers)
    json_data = json.loads(rv.data)
    assert json_data['es_favorita'] == False

    Cancion.query.delete()
    Usuario.query.delete()
    db.session.commit()

def test_agregar_cancion_con_genero_correcto(client, sign_in):
    sign_in_data = sign_in
    user = sign_in_data["user"]
    headers = {
            "Authorization": "Bearer {}".format(sign_in_data["token"]),
            "Content-Type": "application/json"
            }

    data = {
            "titulo": "Test new song",
            "minutos": "10",
            "segundos": "30",
            "interprete": "Test interprete",
            "es_favorita": True,
            "genero": "BALADAS"
            }

    rv = client.post(
            '/usuario/' + str(user.id) + '/canciones',
            data=json.dumps(data),
            headers=headers,
            )
    json_data = json.loads(rv.data)

    assert json_data['titulo'] == data['titulo']
    assert json_data['interprete'] == data['interprete']
    assert json_data['genero']['llave'] == data['genero']

    Cancion.query.delete()
    Usuario.query.delete()
    db.session.commit()

def test_agregar_cancion_con_genero_incorrecto(client, sign_in):
    sign_in_data = sign_in
    user = sign_in_data["user"]
    headers = {
            "Authorization": "Bearer {}".format(sign_in_data["token"]),
            "Content-Type": "application/json"
            }
    data = {
            "titulo": "Test new song",
            "minutos": "10",
            "segundos": "30",
            "interprete": "Test interprete",
            "es_favorita": True,
            "genero": "GENERO_INCORRECTO"
            }

    with pytest.raises(Exception) as execinfo: 
        rv = client.post(
                '/usuario/' + str(user.id) + '/canciones',
                data=json.dumps(data),
                headers=headers,
                )

    #Assert that is raised and error with correct message 
    assert str(execinfo.value) == "'GENERO_INCORRECTO' is not among the defined enum values. Enum name: genero. Possible values: BACHATA, BALADAS, BANDA, ..., BOLERO"
    Usuario.query.delete()
    db.session.commit()

def test_ver_cancion_detalle(client, sign_in):
    sign_in_data = sign_in
    user = sign_in_data["user"]
    headers = {
            "Authorization": "Bearer {}".format(sign_in_data["token"]),
            "Content-Type": "application/json"
            }

    nueva_cancion = Cancion(
            titulo="test",
            minutos="10",
            segundos="30",
            interprete="Test interprete",
            es_favorita=True,
            genero="BOLERO",
            usuario=user.id
            )
    db.session.add(nueva_cancion)
    db.session.commit()

    rv = client.get('/cancion/'+str(nueva_cancion.id), headers=headers)
    json_data = json.loads(rv.data)
    assert json_data['id'] == nueva_cancion.id
    assert json_data['genero']['llave'] == "BOLERO"

    Cancion.query.delete()
    Usuario.query.delete()
    db.session.commit()

def test_listar_canciones(client, sign_in):
    sign_in_data = sign_in
    user = sign_in_data["user"]
    headers = {
            "Authorization": "Bearer {}".format(sign_in_data["token"]),
            "Content-Type": "application/json"
            }
    nueva_cancion = Cancion(
            titulo="test",
            minutos="10",
            segundos="30",
            interprete="Test interprete",
            es_favorita=True,
            genero="BOLERO",
            usuario=user.id
            )
    db.session.add(nueva_cancion)
    db.session.commit()

    rv = client.get('/usuario/' +str(user.id) + '/canciones', headers=headers)
    json_data = json.loads(rv.data)
    assert json_data[0]['id'] == nueva_cancion.id
    assert json_data[0]['genero']['llave'] == "BOLERO"

    Cancion.query.delete()
    Usuario.query.delete()
    db.session.commit()

def test_crear_album_with_correct_access_token(client, sign_in):
    sign_in_data = sign_in
    user = sign_in_data["user"]
    headers = {
            "Authorization": "Bearer {}".format(sign_in_data["token"]),
            "Content-Type": "application/json"
            }

    data = {
            "titulo":"test",
            "anio":"2020",
            "descripcion":"Test descripcion",
            "medio":"DISCO"
            }

    response = rv = client.post(
                '/usuario/'+str(user.id)+'/albumes',
                data=json.dumps(data),
                headers=headers,
                )

    json_data = json.loads(rv.data)
    assert json_data["id"] == user.albumes[0].id

    Usuario.query.delete()
    Album.query.delete()
    db.session.commit()

def test_crear_album_with_incorrect_access_token(client, sign_in):
    sign_in_data = sign_in
    user = sign_in_data["user"]
    headers = {
            "Authorization": "Bearer {}".format("abc"),
            "Content-Type": "application/json"
            }

    data = {
            "titulo":"test",
            "anio":"2020",
            "descripcion":"Test descripcion",
            "medio":"DISCO"
            }

    response = rv = client.post(
                '/usuario/'+str(user.id)+'/albumes',
                data=json.dumps(data),
                headers=headers,
                )

    json_data = json.loads(rv.data)
    assert json_data['msg'] == 'Not enough segments'

    Usuario.query.delete()
    Album.query.delete()
    db.session.commit()

def test_get_user_albums(client, sign_in):
    sign_in_data = sign_in
    user = sign_in_data["user"]
    headers = {
            "Authorization": "Bearer {}".format(sign_in_data["token"]),
            "Content-Type": "application/json"
            }
    nuevo_album = Album(
            titulo="Abc",
            anio="2020",
            descripcion="Descripcion",
            medio="DISCO"
            )

    user.albumes.append(nuevo_album) 
    db.session.commit()

    response = rv = client.get(
                '/usuario/'+str(user.id)+'/albumes',
                headers=headers,
                )

    json_data = json.loads(rv.data)

    assert json_data[0]["titulo"] == nuevo_album.titulo
    Usuario.query.delete()
    Album.query.delete()
    db.session.commit()


@pytest.fixture
def sign_in_dos(client):
    nuevo_usuario = Usuario(
            nombre='test_user_dos',
            contrasena='test_user_dos'
            )
    db.session.add(nuevo_usuario)
    db.session.commit()
    response = client.post(
            '/logIn',
            data=json.dumps({"nombre": nuevo_usuario.nombre, "contrasena": nuevo_usuario.contrasena}),
            headers={"Content-Type": "application/json"},
            )
    json_data = json.loads(response.data)
    return {"user": nuevo_usuario, "token": json_data["token"]}

def test_compartir_album(client, sign_in, sign_in_dos):
    sign_in_data = sign_in
    user = sign_in_data["user"]
    sign_in_data_dos = sign_in_dos
    user_dos = sign_in_dos["user"]
    headers = {
            "Authorization": "Bearer {}".format(sign_in_data["token"]),
            "Content-Type": "application/json"
            }

    data = {
            "titulo":"test",
            "anio":"2020",
            "descripcion":"Test descripcion",
            "medio":"DISCO",
            "es_compartido": "False"
            }

    response = rv = client.post(
                '/usuario/'+str(user.id)+'/albumes',
                data=json.dumps(data),
                headers=headers,
                )

    headers_dos = {
            "Authorization": "Bearer {}".format(sign_in_data_dos["token"]),
            "Content-Type": "application/json"
            }

    response_dos = rv_dos = client.post(
                '/usuario/'+str(user_dos.id)+'/albumes/change_shared_state',
                data= json.dumps({"id_album":user.albumes[0].id}),
                headers=headers
                )

    json_data = json.loads(rv.data)
    json_data_dos = json.loads(rv_dos.data)
    assert user.id == 1
    assert user_dos.id == 2
    assert user.albumes[0].id == 1
    assert user_dos.albumes[0].id == 2
    assert user_dos.albumes[0].es_compartido == True
    assert json_data_dos['es_compartido'] == True
    
    Usuario.query.delete()
    Album.query.delete()
    db.session.commit()

def test_compartir_cancion(client, sign_in, sign_in_dos):
    db.session.execute("DELETE FROM cancion_usuario")
    user_1_data = sign_in
    user_2_data = sign_in_dos
    user_uno = user_1_data["user"]
    user_dos = user_2_data["user"]

    headers_user1 = {
            "Authorization": "Bearer {}".format(user_1_data["token"]),
            "Content-Type": "application/json"
            }

    cancion_data_user1 = Cancion(
        titulo="test",
        minutos="10",
        segundos="30",
        interprete="Test interprete",
        genero="BOLERO",
        usuario=user_uno.id
        )
    db.session.add(cancion_data_user1)
    db.session.commit()

    data_song_shared={
        "id_cancion":cancion_data_user1.id,
        "id_shared_user":user_dos.id,
    }

    rv_share_song_to_user2= client.post(
        '/usuario/' + str(user_uno.id) + '/canciones/song_shared',
        data=json.dumps(data_song_shared),
        headers=headers_user1
    )

    shared_song = user_dos.canciones[0]

    assert shared_song.es_compartida == True
    assert shared_song.id_original == cancion_data_user1.id

    Usuario.query.delete()
    Cancion.query.delete()
    db.session.commit()

def test_compartir_cancion_mismo_usuario(client, sign_in, sign_in_dos):
    user_1_data = sign_in
    user_uno = user_1_data["user"]

    headers_user1 = {
            "Authorization": "Bearer {}".format(user_1_data["token"]),
            "Content-Type": "application/json"
            }

    cancion_data_user1 = Cancion(
        titulo="test",
        minutos="10",
        segundos="30",
        interprete="Test interprete",
        genero="BOLERO",
        usuario=user_uno.id
        )
    db.session.add(cancion_data_user1)
    db.session.commit()

    data_song_shared={
        "id_cancion":cancion_data_user1.id,
        "id_shared_user":user_uno.id,
    }

    rv_share_song_to_user2= client.post(
        '/usuario/' + str(user_uno.id) + '/canciones/song_shared',
        data=json.dumps(data_song_shared),
        headers=headers_user1
    )

    json_data = json.loads(rv_share_song_to_user2.data)
    assert json_data == "No se puede compartir la cancion "+ str(cancion_data_user1.id) + " con el mismo usuario " + str(user_uno.id)

    Usuario.query.delete()
    Cancion.query.delete()
    db.session.commit()

def test_crear_comentario(client, sign_in):
    user_1_data = sign_in
    user_uno = user_1_data["user"]

    headers_user1 = {
            "Authorization": "Bearer {}".format(user_1_data["token"]),
            "Content-Type": "application/json"
            }

    cancion_data_user1 = Cancion(
        titulo="test",
        minutos="10",
        segundos="30",
        interprete="Test interprete",
        genero="BOLERO",
        usuario=user_uno.id
        )
    db.session.add(cancion_data_user1)
    db.session.commit()

    comentario={
        "content": "Super comentario",
        "creada": "Creada",
        "usuario":user_uno.id,
    }

    response = client.post(
        '/cancion/' + str( cancion_data_user1.id)+ '/comentarios',
        data=json.dumps(comentario),
        headers=headers_user1
    )

    json_data = json.loads(response.data)

    assert json_data["content"] == comentario["content"]

    Usuario.query.delete()
    Cancion.query.delete()
    Comentario.query.delete()
    db.session.commit()
