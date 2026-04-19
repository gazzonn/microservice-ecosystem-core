# microservice-ecosystem-core

Учебное ядро цифровой экосистемы на основе микросервисной архитектуры для дипломного проекта.

## О проекте

Проект реализует базовое ядро экосистемы, которое можно использовать как основу для разных цифровых сервисов. В текущей версии уже работают:

- единая точка входа через `api_gateway`;
- аутентификация и выдача JWT в `auth_service`;
- ролевая авторизация в `authorization_service`;
- управление пользователями в `user_service`;
- реестр сервисов и маршрутов в `service_registry`;
- демонстрационный сервис `demo_microservice`;
- общие модули в `shared`;
- инфраструктура на `Docker Compose` с `PostgreSQL` и `Redis`.

## Технологический стек

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Redis
- Docker / Docker Compose
- JWT
- Pydantic
- Uvicorn

## Структура репозитория

```text
microservice-ecosystem-core/
├── api_gateway/
├── auth_service/
├── authorization_service/
├── demo_microservice/
├── service_registry/
├── shared/
├── user_service/
├── .env
├── .env.example
├── docker-compose.yml
└── README.md
```

## Сервисы

### API Gateway

Назначение:
единая точка входа в систему.

Ключевые возможности:
- маршрутизация запросов к внутренним сервисам;
- проверка access token;
- проверка доступа через `authorization_service`;
- проксирование запросов в зарегистрированные микросервисы;
- базовое ограничение частоты запросов.

Основные endpoint:
- `GET /health`
- `GET /routes`
- `ANY /gateway/{path:path}`

### Auth Service

Назначение:
регистрация, логин, refresh token, logout и валидация токена.

Основные endpoint:
- `POST /auth/register`
- `POST /auth/login`
- `POST /auth/refresh`
- `POST /auth/logout`
- `POST /auth/validate`
- `POST /auth/change-password`

### Authorization Service

Назначение:
работа с ролями и permissions.

Основные endpoint:
- `POST /authorize/check`
- `GET /authorize/user/{user_id}/roles`
- `GET /authorize/user/{user_id}/permissions`
- `POST /authorize/roles`
- `POST /authorize/permissions`
- `POST /authorize/assign-role`
- `POST /authorize/assign-permission`

### User Service

Назначение:
CRUD-операции с пользователями.

Основные endpoint:
- `POST /users`
- `GET /users`
- `GET /users/{id}`
- `PUT /users/{id}`
- `DELETE /users/{id}`
- `PATCH /users/{id}/block`
- `PATCH /users/{id}/unblock`

### Service Registry

Назначение:
хранение информации о подключённых сервисах и маршрутах.

Основные endpoint:
- `POST /services/register`
- `DELETE /services/{id}`
- `GET /services`
- `GET /services/{name}`
- `PATCH /services/{id}/status`
- `GET /services/resolve/route?path=/demo/public&method=GET`

### Demo Microservice

Назначение:
демонстрация работы экосистемы через публичные и защищённые маршруты.

Основные endpoint:
- `GET /demo/public`
- `GET /demo/private`
- `GET /demo/admin`
- `GET /` — demo UI для показа на защите

## Запуск проекта

### Требования

Нужны:
- Docker Desktop;
- запущенный Docker Engine.

`pgAdmin 4` не обязателен. База данных поднимается автоматически через `docker compose`.

### Быстрый старт

Из корня проекта выполните:

```bash
docker compose up --build
```

После запуска будут доступны:

- `http://localhost:8000` — API Gateway
- `http://localhost:8001` — Auth Service
- `http://localhost:8002` — Authorization Service
- `http://localhost:8003` — User Service
- `http://localhost:8004` — Service Registry
- `http://localhost:8005` — Demo Microservice и demo UI

Проверка состояния контейнеров:

```bash
docker compose ps
```

Health-check сервисов:

```bash
curl http://localhost:8000/health
curl http://localhost:8001/health
curl http://localhost:8002/health
curl http://localhost:8003/health
curl http://localhost:8004/health
curl http://localhost:8005/health
```

## Swagger UI

Для ручной проверки API можно открыть:

- `http://localhost:8000/docs`
- `http://localhost:8001/docs`
- `http://localhost:8002/docs`
- `http://localhost:8003/docs`
- `http://localhost:8004/docs`
- `http://localhost:8005/docs`

## Demo UI

Основная страница для демонстрации находится по адресу:

- `http://localhost:8005/`

На странице доступны:
- вызовы `public`, `private`, `admin` через gateway;
- регистрация пользователя;
- логин с получением токена;
- создание и назначение роли;
- создание и назначение permission;
- просмотр отправленного JSON-запроса и ответа сервиса.

Слева отображаются текущие значения состояния:
- `user_id`;
- `role_id`;
- `permission_id`;
- `access_token`.

## Важная подготовка перед demo flow

Для работы маршрутов через gateway demo-сервис должен быть зарегистрирован в `service_registry`.

Это можно сделать один раз через `http://localhost:8004/docs` и endpoint `POST /services/register` со следующим JSON:

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

## Рекомендуемый сценарий демонстрации

### Позитивный сценарий

1. Открыть `http://localhost:8005/`.
2. Зарегистрировать пользователя.
3. Выполнить вход.
4. Создать роль `ADMIN`.
5. Назначить роль пользователю.
6. Создать permission для `demo:read_admin`.
7. Назначить permission роли.
8. Показать успешный вызов:
   - `Public`
   - `Private`
   - `Admin`

### Негативный сценарий

На той же странице можно показать:
- `Private без токена` -> ожидается `401`;
- `Admin без токена` -> ожидается `401`;
- если не назначать роль или permission, то `Admin` должен вернуть отказ доступа.

## Формат ответа API

Успешный ответ:

```json
{
  "success": true,
  "message": "Request processed successfully",
  "data": {},
  "timestamp": "2026-04-07T12:00:00Z"
}
```

Ответ с ошибкой:

```json
{
  "success": false,
  "message": "Unauthorized",
  "error_code": "AUTH_401",
  "details": {},
  "timestamp": "2026-04-07T12:00:00Z"
}
```

## Текущее состояние MVP

Сейчас в проекте реализованы:
- базовая микросервисная структура в одном monorepo;
- единая конфигурация и общие модули в `shared`;
- JWT access/refresh token;
- хэширование паролей;
- role-based access control;
- service registry и gateway routing;
- demo UI для защиты;
- health endpoint у сервисов;
- Docker Compose для локального запуска.

## Ограничения текущей версии

- миграции Alembic пока не подключены;
- таблицы создаются через `Base.metadata.create_all(...)`;
- Redis поднят в инфраструктуре, но используется не во всех сценариях;
- автoрегистрация сервисов в registry пока не реализована;
- тесты `pytest` пока не добавлены;
- часть demo-данных удобнее создавать вручную через UI или Swagger.

## Что можно развивать дальше

- добавить Alembic и миграции;
- вынести revoke/blacklist токенов в Redis;
- добавить audit logs;
- покрыть ключевые сценарии `pytest`-тестами;
- реализовать автоматическую регистрацию сервисов в registry;
- расширить demo UI негативными сценариями с блокировкой пользователя и вторым пользователем без роли.
