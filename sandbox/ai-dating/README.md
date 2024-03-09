
# AI Dating

Welcome to AI Dating. This is our sandbox to play with ChatGPT Operations

## Set-up

Run
```sh
scripts/bootstrap
```
to set-up the virtual environment.

There is configuration for VSCode in this repo, otherwise you're on your own.

Add `.env.local` with `OPENAI_API_KEY=<key>`

Run
```sh
docker compose build
docker compose up
```

If everything worked, you should be able to navigate to `localhost/healthz`

## VSCode

https://code.visualstudio.com/docs/python/environments

## Technical Infrastructure

A good place to start is with `docker-compose.yaml`. This shows the three services that we run nginx, db, and ai-dating. nginx is our proxy, postgres is our db, and ai-dating is Python Fast API App.

From here, looking at the `Dockerfile` will show the entrypoint for our Flask App.

You can run `docker logs -f nginx`, `docker logs -f db`, `docker logs -f ai-dating` to see logs.

Run
 ```sh
docker compose exec db psql --username=ai_dating --dbname=ai_dating_dev
```
to access the Database


Alembic for migrations. See `entrypoint.sh`

## References

We'll probably want to change the `message` table a bit to have indices and stuff
https://api.python.langchain.com/en/latest/_modules/langchain_community/chat_message_histories/postgres.html#PostgresChatMessageHistory

# TODO

Migrations clean up

Hook up Front-end

Host DB

Deploy non-locally

Add precommit hooks

Add user to message log
