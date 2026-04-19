from fastapi import APIRouter
from fastapi.responses import HTMLResponse, JSONResponse

from demo_microservice.app.schemas.ui import (
    AssignPermissionPayload,
    AssignRolePayload,
    GatewayRequestPayload,
    PermissionPayload,
    RolePayload,
    UserLoginPayload,
    UserRegisterPayload,
)
from demo_microservice.app.services.demo_console_service import DemoConsoleService


router = APIRouter(tags=["demo_ui"])
service = DemoConsoleService()


DEMO_HTML = """
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Microservice Ecosystem Demo</title>
  <style>
    :root {
      --bg: #f4efe7;
      --panel: #fffaf2;
      --ink: #1f2937;
      --muted: #6b7280;
      --accent: #b45309;
      --accent-2: #0f766e;
      --danger: #b91c1c;
      --border: #e7dccb;
      --shadow: 0 18px 45px rgba(84, 59, 20, 0.12);
      --radius: 22px;
    }

    * { box-sizing: border-box; }

    body {
      margin: 0;
      font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
      background:
        radial-gradient(circle at top left, rgba(180, 83, 9, 0.15), transparent 30%),
        radial-gradient(circle at top right, rgba(15, 118, 110, 0.14), transparent 25%),
        linear-gradient(180deg, #f8f2e8 0%, #f3ece2 100%);
      color: var(--ink);
    }

    .page {
      width: min(1380px, calc(100% - 28px));
      margin: 24px auto 36px;
    }

    .hero {
      background: linear-gradient(135deg, rgba(180, 83, 9, 0.92), rgba(15, 118, 110, 0.9));
      color: white;
      border-radius: 32px;
      padding: 26px 24px;
      box-shadow: var(--shadow);
      margin-bottom: 22px;
      text-align: center;
    }

    .hero h1 {
      margin: 0;
      font-size: clamp(30px, 4vw, 50px);
      line-height: 1.05;
    }

    .layout {
      display: grid;
      grid-template-columns: 260px minmax(420px, 1fr) minmax(360px, 430px);
      gap: 18px;
      align-items: start;
    }

    .panel {
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 18px;
      box-shadow: var(--shadow);
    }

    .panel h2 {
      margin: 0 0 12px;
      font-size: 24px;
    }

    .state-stack {
      display: grid;
      gap: 12px;
    }

    .pill {
      background: rgba(255,255,255,0.78);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 12px 14px;
      min-width: 0;
      overflow: hidden;
    }

    .pill strong {
      display: block;
      margin-bottom: 6px;
      font-size: 12px;
      color: var(--muted);
      text-transform: uppercase;
      letter-spacing: 0.06em;
    }

    .pill span {
      display: block;
      overflow-wrap: anywhere;
      word-break: break-word;
      line-height: 1.45;
      font-size: 14px;
    }

    .demo-stack {
      display: grid;
      gap: 16px;
    }

    .step {
      border: 1px solid var(--border);
      border-radius: 18px;
      padding: 16px;
      background: rgba(255,255,255,0.62);
    }

    .step h3 {
      margin: 0 0 12px;
      font-size: 22px;
    }

    label {
      display: block;
      margin-bottom: 10px;
      font-size: 14px;
      color: var(--muted);
    }

    input {
      width: 100%;
      margin-top: 6px;
      padding: 12px 14px;
      border-radius: 14px;
      border: 1px solid var(--border);
      background: #fffdf9;
      color: var(--ink);
      font: inherit;
    }

    .actions {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 12px;
    }

    button {
      border: 0;
      border-radius: 999px;
      padding: 11px 16px;
      font: inherit;
      font-weight: 700;
      color: white;
      background: var(--accent);
      cursor: pointer;
      transition: transform .15s ease, opacity .15s ease;
    }

    button.secondary { background: var(--accent-2); }
    button.danger { background: var(--danger); }
    button:hover { transform: translateY(-1px); }

    .logs {
      display: grid;
      gap: 16px;
    }

    pre {
      margin: 0;
      padding: 16px;
      border-radius: 18px;
      background: #1f2937;
      color: #f9fafb;
      overflow: auto;
      min-height: 260px;
      white-space: pre-wrap;
      word-break: break-word;
    }

    @media (max-width: 1160px) {
      .layout {
        grid-template-columns: 1fr;
      }
    }
  </style>
</head>
<body>
  <div class="page">
    <section class="hero">
      <h1>Microservice Ecosystem Demo Console</h1>
    </section>

    <section class="layout">
      <aside class="panel">
        <div class="state-stack">
          <div class="pill"><strong>User ID</strong><span id="state-user-id">not set</span></div>
          <div class="pill"><strong>Role ID</strong><span id="state-role-id">not set</span></div>
          <div class="pill"><strong>Permission ID</strong><span id="state-permission-id">not set</span></div>
          <div class="pill"><strong>Access Token</strong><span id="state-token">not set</span></div>
        </div>
      </aside>

      <main class="panel">
        <div class="demo-stack">
          <section class="step">
            <h3>Gateway</h3>
            <div class="actions">
              <button onclick="gatewayCall('/demo/public', false)">Public</button>
              <button class="secondary" onclick="gatewayCall('/demo/private', true)">Private</button>
              <button class="secondary" onclick="gatewayCall('/demo/admin', true)">Admin</button>
            </div>
          </section>

          <section class="step">
            <h3>Регистрация</h3>
            <label>Username<input id="register-username" value="demo_user" /></label>
            <label>Email<input id="register-email" value="demo_user@example.com" /></label>
            <label>Password<input id="register-password" type="password" value="StrongPass123!" /></label>
            <div class="actions">
              <button onclick="registerUser()">Зарегистрироваться</button>
            </div>
          </section>

          <section class="step">
            <h3>Вход</h3>
            <label>Username<input id="login-username" value="demo_user" /></label>
            <label>Password<input id="login-password" type="password" value="StrongPass123!" /></label>
            <div class="actions">
              <button class="secondary" onclick="loginUser()">Войти</button>
            </div>
          </section>

          <section class="step">
            <h3>Роль</h3>
            <label>Role name<input id="role-name" value="ADMIN" /></label>
            <div class="actions">
              <button onclick="createRole()">Создать роль</button>
              <button class="secondary" onclick="assignRole()">Назначить роль</button>
            </div>
          </section>

          <section class="step">
            <h3>Permission</h3>
            <label>Permission name<input id="permission-name" value="Read demo admin endpoint" /></label>
            <div class="actions">
              <button onclick="createPermission()">Создать permission</button>
              <button class="secondary" onclick="assignPermission()">Назначить permission</button>
            </div>
          </section>
        </div>
      </main>

      <aside class="panel">
        <div class="logs">
          <pre id="request-log">Нажмите любую кнопку, чтобы увидеть запрос.</pre>
          <pre id="response-log">Ответ сервиса появится здесь.</pre>
        </div>
      </aside>
    </section>
  </div>

  <script>
    const state = {
      userId: "",
      roleId: "",
      permissionId: "",
      accessToken: "",
    };

    function updateState() {
      document.getElementById("state-user-id").textContent = state.userId || "not set";
      document.getElementById("state-role-id").textContent = state.roleId || "not set";
      document.getElementById("state-permission-id").textContent = state.permissionId || "not set";
      document.getElementById("state-token").textContent = state.accessToken ? state.accessToken.slice(0, 28) + "..." : "not set";
    }

    function showExchange(title, status, requestPayload, responsePayload) {
      document.getElementById("request-log").textContent = JSON.stringify({ action: title, request: requestPayload }, null, 2);
      document.getElementById("response-log").textContent = JSON.stringify({ action: title, status_code: status, response: responsePayload }, null, 2);
    }

    async function sendRequest(title, url, body) {
      const requestPayload = body || {};
      const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(requestPayload),
      });
      const payload = await response.json();
      showExchange(title, response.status, requestPayload, payload);
      return { response, payload };
    }

    async function registerUser() {
      const requestPayload = {
        username: document.getElementById("register-username").value,
        email: document.getElementById("register-email").value,
        password: document.getElementById("register-password").value,
      };
      const result = await sendRequest("register user", "/ui/register", requestPayload);
      state.userId = result.payload?.payload?.data?.user_id || state.userId;
      updateState();
    }

    async function loginUser() {
      const requestPayload = {
        username: document.getElementById("login-username").value,
        password: document.getElementById("login-password").value,
      };
      const result = await sendRequest("login", "/ui/login", requestPayload);
      const data = result.payload?.payload?.data || {};
      state.userId = data.user_id || state.userId;
      state.accessToken = data.access_token || "";
      updateState();
    }

    async function createRole() {
      const requestPayload = {
        name: document.getElementById("role-name").value,
        description: "Administrator role for diploma demo",
      };
      const result = await sendRequest("create role", "/ui/roles", requestPayload);
      state.roleId = result.payload?.payload?.data?.id || state.roleId;
      updateState();
    }

    async function createPermission() {
      const requestPayload = {
        name: document.getElementById("permission-name").value,
        resource: "demo",
        action: "read_admin",
        description: "Access to /demo/admin",
      };
      const result = await sendRequest("create permission", "/ui/permissions", requestPayload);
      state.permissionId = result.payload?.payload?.data?.id || state.permissionId;
      updateState();
    }

    async function assignRole() {
      await sendRequest("assign role", "/ui/assign-role", {
        user_id: state.userId,
        role_id: state.roleId,
      });
    }

    async function assignPermission() {
      await sendRequest("assign permission", "/ui/assign-permission", {
        role_id: state.roleId,
        permission_id: state.permissionId,
      });
    }

    async function gatewayCall(path, withToken) {
      await sendRequest(`gateway ${path}`, "/ui/gateway-request", {
        path,
        token: withToken ? state.accessToken : null,
      });
    }

    updateState();
  </script>
</body>
</html>
"""


@router.get("/", response_class=HTMLResponse)
async def demo_console() -> HTMLResponse:
    return HTMLResponse(DEMO_HTML)


@router.post("/ui/register")
async def register_user(payload: UserRegisterPayload) -> JSONResponse:
    result = await service.register_user(payload.model_dump())
    return JSONResponse(status_code=result["status_code"], content=result)


@router.post("/ui/login")
async def login_user(payload: UserLoginPayload) -> JSONResponse:
    result = await service.login_user(payload.model_dump())
    return JSONResponse(status_code=result["status_code"], content=result)


@router.post("/ui/roles")
async def create_role(payload: RolePayload) -> JSONResponse:
    result = await service.create_role(payload.model_dump())
    return JSONResponse(status_code=result["status_code"], content=result)


@router.post("/ui/permissions")
async def create_permission(payload: PermissionPayload) -> JSONResponse:
    result = await service.create_permission(payload.model_dump())
    return JSONResponse(status_code=result["status_code"], content=result)


@router.post("/ui/assign-role")
async def assign_role(payload: AssignRolePayload) -> JSONResponse:
    result = await service.assign_role(payload.model_dump())
    return JSONResponse(status_code=result["status_code"], content=result)


@router.post("/ui/assign-permission")
async def assign_permission(payload: AssignPermissionPayload) -> JSONResponse:
    result = await service.assign_permission(payload.model_dump())
    return JSONResponse(status_code=result["status_code"], content=result)


@router.post("/ui/gateway-request")
async def gateway_request(payload: GatewayRequestPayload) -> JSONResponse:
    result = await service.call_gateway(path=payload.path, token=payload.token)
    return JSONResponse(status_code=result["status_code"], content=result)



