# catalogoPelisFlask

[Flask-Assistant](https://github.com/treethought/flask-assistant) based webhook deployed to Heroku to fulfillment Dialogflow application to search a film title in a Google spreadsheet.

The spreadsheet must have two columns: film location and film title.

Docker image based on Heroku Alpine-based Docker example

### Test

```
docker build -t catalogo:latest . && docker run -p 5000:5000 --env-file .env --rm -it  --name catalogo --entrypoint=./test.sh catalogo
```

### Run

```
docker build -t catalogo:latest . && docker run -p 5000:5000 --env-file .env --rm  --name catalogo catalogo
```

### .env file

```
GOOGLE_PRIVATE_KEY=-----BEGIN PRIVATE KEY-----\n.....\n-----END PRIVATE KEY-----\n
GOOGLE_CLIENT_EMAIL=any@any.iam.gserviceaccount.com
GOOGLE_SPREADSHEET_ID=any
GOOGLE_SPREADSHEET_RANGE=A2:B900
PORT=5000
```

### Deploy to Heroku

```
heroku container:push web --app catalogo-pelis-flask 

heroku config:set GOOGLE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n.....\n-----END PRIVATE KEY-----\n" --app catalogo-pelis-flask
heroku config:set GOOGLE_CLIENT_EMAIL="any@any.iam.gserviceaccount.com" --app catalogo-pelis-flask
heroku config:set GOOGLE_SPREADSHEET_ID="any" --app catalogo-pelis-flask
heroku config:set GOOGLE_SPREADSHEET_RANGE="A2:B900" --app catalogo-pelis-flask

heroku container:release web --app catalogo-pelis-flask
```

### Notes

[Flask-Assistant](https://github.com/treethought/flask-assistant) [improved](https://github.com/jose-carmona/flask-assistant) to support Dependency Injection with [Injector](https://github.com/alecthomas/injector)

