# MicroserviceEcosystemCore

Учебное ядро цифровой экосистемы на основе микросервисной архитектуры для дипломного проекта.

## Что реализовано

- `api_gateway` как единая точка входа
- `auth_service` для регистрации, логина, JWT access/refresh token и logout
- `authorization_service` для ролей, permissions и проверки доступа
- `user_service` для CRUD-управления пользователями
- `service_registry` для регистрации сервисов и маршрутов
- `demo_microservice` для демонстрации публичных и защищённых endpoint
- `shared` с общей конфигурацией, БД, схемами ответов, безопасностью и исключениями
- `docker-compose.yml` для PostgreSQL, Redis и всех сервисов

## Структура проекта

```text
MicroserviceEcosystemCore/
├── api_gateway/
├── auth_service/
├── authorization_service/
├── demo_microservice/
├── service_registry/
├── shared/
├── user_service/
├── .env
├── .env.example
└── docker-compose.yml
```

## Архитектурная идея

- Каждый сервис отвечает только за одну предметную область.
- Взаимодействие между сервисами идёт через HTTP API.
- `API Gateway` не хранит бизнес-логику, а валидирует токен, проверяет доступ и проксирует запрос.
- Новый сервис можно подключить через `Service Registry`, зарегистрировав его `base_url` и маршруты.
- Ответы приведены к единому формату `SuccessResponse` и `ErrorResponse`.

## Основные endpoint'ы

### Auth Service

- `POST /auth/register`
- `POST /auth/login`
- `POST /auth/refresh`
- `POST /auth/logout`
- `POST /auth/validate`
- `POST /auth/change-password`

### Authorization Service

- `POST /authorize/check`
- `GET /authorize/user/{user_id}/roles`
- `GET /authorize/user/{user_id}/permissions`
- `POST /authorize/roles`
- `POST /authorize/permissions`
- `POST /authorize/assign-role`
- `POST /authorize/assign-permission`

### User Service

- `POST /users`
- `GET /users`
- `GET /users/{id}`
- `PUT /users/{id}`
- `DELETE /users/{id}`
- `PATCH /users/{id}/block`
- `PATCH /users/{id}/unblock`

### Service Registry

- `POST /services/register`
- `DELETE /services/{id}`
- `GET /services`
- `GET /services/{name}`
- `PATCH /services/{id}/status`
- `GET /services/resolve/route?path=/demo/public&method=GET`

### API Gateway

- `GET /health`
- `GET /routes`
- `/gateway/{path:path}`

### Demo Microservice

- `GET /demo/public`
- `GET /demo/private`
- `GET /demo/admin`

## Быстрый запуск

1. Убедитесь, что установлен Docker и Docker Compose.
2. Из корня проекта выполните:

```bash
docker compose up --build
```

3. После запуска сервисы будут доступны:

- `http://localhost:8000` - API Gateway
- `http://localhost:8001` - Auth Service
- `http://localhost:8002` - Authorization Service
- `http://localhost:8003` - User Service
- `http://localhost:8004` - Service Registry
- `http://localhost:8005` - Demo Microservice

## Рекомендуемый demo flow

1. Зарегистрировать пользователя через `auth_service`.
2. Выполнить логин и получить `access_token` и `refresh_token`.
3. Создать роль `ADMIN` и permission, например `demo:read_admin`.
4. Назначить роль пользователю и permission роли.
5. Зарегистрировать demo-сервис в `service_registry`.

Пример регистрации `demo_microservice`:

```json
{
  "name": "demo_microservice",
  "base_url": "http://demo_microservice:8005",
  "health_url": "http://demo_microservice:8005/health",
  "status": "ACTIVE",
  "version": "1.0.0",
  "routes": [
    {
      "path": "/demo/public",
      "method": "GET",
      "is_protected": false,
      "required_permission": null
    },
    {
      "path": "/demo/private",
      "method": "GET",
      "is_protected": true,
      "required_permission": null
    },
    {
      "path": "/demo/admin",
      "method": "GET",
      "is_protected": true,
      "required_permission": "demo:read_admin"
    }
  ]
}
```

6. Открыть через gateway:

- `GET /gateway/demo/public`
- `GET /gateway/demo/private`
- `GET /gateway/demo/admin`

## Ограничения текущего MVP

- Миграции Alembic пока не добавлены, таблицы создаются через `Base.metadata.create_all`.
- Redis подготовлен в инфраструктуре, но blacklist token пока хранится в PostgreSQL.
- Логирование реализовано на базовом уровне через стандартный `logging`.
- Автоматическая self-registration сервисов в registry пока не настроена.

## Что удобно развивать дальше

- добавить Alembic и отдельные схемы БД;
- перенести revoke/blacklist refresh token в Redis;
- добавить audit logs и централизованный мониторинг;
- покрыть сценарии `pytest`-тестами;
- расширить gateway health-check логикой проверки доступности сервисов.
