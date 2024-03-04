
# AI Dating

Welcome to AI Dating. This is our sandbox to play with ChatGPT Operations

## Set-up

Run
```sh
scripts/bootstrap
```
to set-up the virtual environment.

There is configuration for VSCode in this repo, otherwise you're on your own.

Run
```sh
docker compose build
docker compose up
```

If everything worked, you should be able to navigate to `localhost/healthz`

## Technical Infrastructure

A good place to start is with `docker-compose.yaml`. This shows the three services that we run nginx, db, and ai-dating. nginx is our proxy, postgres is our db, and ai-dating is Python Flask App.

From here, looking at the `Dockerfile` will show the entrypoint for our Flask App.

You can run `docker logs -f nginx`, `docker logs -f db`, `docker logs -f ai-dating` to see logs.

Run
 ```sh
docker compose exec db psql --username=ai_dating --dbname=ai_dating_dev
```
to access the Database

Migrations are still a bit of a mess, but right now you can edit `entrypoint.sh` to run `flask migrate -m "<migration_message>"` and `flask db upgrade`

# TODO
Auto-reload on save

Pipe Logs

Dev ENV File

Migrations clean up

Hook up Front-end
