# Translator prototype application


## Project Setup

```sh
cp .env.example .env
```

Then edit .env file to set up application port and translation API key.

Finally:

```sh
docker-compose up -d --build
```

## Open application

Run your browset and go to http://127.0.0.1:${LINGVANEX_PORT}
