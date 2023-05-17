## Local development

```
docker compose up --build
cd ui
npm install # only once
npm run start
```

## Deploying to ECS

Update the image tag as necessary.

```
DOCKER_DEFAULT_PLATFORM=linux/amd64 docker compose -f docker-compose.yml -f docker-compose-ui.yml build
docker compose -f docker-compose.yml -f docker-compose-ui.yml push
docker context create ecs myecscontext # once
docker context use myecscontext
docker compose -f docker-compose.yml -f docker-compose-ui.yml up -d
```
