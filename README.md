# Sanic project
Проект написан с помощью фреймворка sanic и sqlachemy[async]
# Для запуска в Docker:

```shell
docker-compose build
docker-compose up -d
```

Для отправки запросов использовать http://localhost:8000

# Для запуска миграции:

```shell
docker exec sanic-backend-1 alembic upgrade head
```
