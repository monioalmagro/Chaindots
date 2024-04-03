```markdown
# Chaindots

Este es el repositorio del proyecto Chaindots.

## Clonar el repositorio

Si deseas probar el proyecto, puedes clonar el repositorio usando el siguiente comando:

```bash
git clone https://github.com/monioalmagro/Chaindots.git
```

## Configuración del entorno virtual (Opción 1)

Para trabajar en un entorno virtual y aislar las dependencias del proyecto, sigue estos pasos:

1. **Instalar el entorno virtual:**

```bash
pip install virtualenv
```

2. **Crear y activar el entorno virtual:**

```bash
virtualenv venv 
source venv/bin/activate 
```

3. **Instalar las dependencias del proyecto:**

```bash
pip install -r requirements.txt
```

4. **Aplicar las migraciones de la base de datos:**

```bash
python manage.py migrate
```

5. **Crear un superusuario (opcional):**

```bash
python manage.py createsuperuser
```
```bash
python manage.py runserver
```
6. **Importa la colección de Postman `Chaindots.postman_collection.json`.**

En la carpeta Token se encuentra la request token en donde con el usuario 
y password antes creado se podra acceder a un token para su posterior configuracion
en la collection y poder ejecutar todos los requests.

## Test


## Ejecutar las pruebas

Para ejecutar las pruebas, sigue estos pasos:

1. Configura el entorno de test:

```bash
export DJANGO_SETTINGS_MODULE=config.setting.tests
```

2. Aplica las migraciones(unica vez) de la base de datos en el entorno de test:

```bash
python manage.py migrate 
```

3. Carga los datos necesarios para las pruebas(unica vez):

```bash
python manage.py loaddata tests/fixtures/json/User.json
python manage.py loaddata tests/fixtures/json/Post.json
python manage.py loaddata tests/fixtures/json/Comment.json
```


4. correr los tests

```bash
python manage.py pytest
```

## Ejecutar la aplicación con docker 

Para ejecutar la aplicación usando Docker, sigue estos pasos:

1. Levantar el compose

```bash
docker compose up
```
2. migrar y super user
```bash
docker exec -it chaindots-web-1 python manage.py migrate
docker exec -it chaindots-web-1 python manage.py createsuperuser
```

3. **Importa la colección de Postman `Chaindots.postman_collection.json`.**

En la carpeta Token se encuentra la request token en donde con el usuario 
y password antes creado se podra acceder a un token para su posterior configuracion
en la collection y poder ejecutar todos los requests.

# tests

3. Migracion y carga de datos.
```bash
docker exec -it chaindots-web-1 bash -c "DJANGO_SETTINGS_MODULE=config.setting.tests python manage.py migrate"

docker exec -it chaindots-web-1 bash -c "DJANGO_SETTINGS_MODULE=config.setting.tests python manage.py loaddata User.json"\n
docker exec -it chaindots-web-1 bash -c "DJANGO_SETTINGS_MODULE=config.setting.tests python manage.py loaddata Post.json"\n
docker exec -it chaindots-web-1 bash -c "DJANGO_SETTINGS_MODULE=config.setting.tests python manage.py loaddata Comment.json"\n
```

6. Correr tests
```bash
docker exec -it chaindots-web-1 bash -c "DJANGO_SETTINGS_MODULE=config.setting.tests pytest"
```


## Nota de author:
En la aplicación, siempre se priorizó realizar el menor número posible de consultas a la base de datos para mantener un rendimiento adecuado. Se implementaron optimizaciones que permiten escalar el código de manera eficiente. Además, se manejaron excepciones de forma pertinente para garantizar la robustez del sistema. La intención fue asegurar que el código resultante fuera legible y de fácil interpretación. Se cumplieron todos los requerimientos cuidando meticulosamente la implementación del mismo.
# detalles de implementacion:

```python
post = Post.objects.get(pk=id)
comments = post.post_comment_set.all().order_by("-created_at")[
    : constants.COMMENTS_BY_POST
]
```
cacheo de errores e implementacion de schemas con pydantyc  
```python
def post(self, request, id, format=None):
    try:
        data = request.data

        comment_data = CommentCreateSchema(**data)

        user, post = get_user_and_post(comment_data.author_id, id)

        comment = create_comment(user, post, comment_data.comment)
        return Response(serializer_data(comment), status=201)
    except ValidationError as error:
        return Response({"error": error.errors()}, status=400)
    except AssertionError as error:
        return Response({"error": str(error)}, status=400)
```
```python
@staticmethod
def get_post_count(user):
    return user.post_set.all().count()

@staticmethod
def get_comments_count(user):
    return user.comment_set.all().count()
```