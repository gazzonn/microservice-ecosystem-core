import pytest

from service_registry.app.models.api_route import ApiRoute
from service_registry.app.models.service import ServiceEntity
from service_registry.app.schemas.registry import ApiRouteCreateRequest, ServiceRegisterRequest
from service_registry.app.services.service_registry_service import ServiceRegistryService
from shared.exceptions.api import NotFoundException


class FakeServiceRepository:
    def __init__(self) -> None:
        self.services: dict[str, ServiceEntity] = {}
        self.routes: dict[str, ApiRoute] = {}

    def create_service(self, service: ServiceEntity) -> ServiceEntity:
        self.services[service.id] = service
        return service

    def create_route(self, route: ApiRoute) -> ApiRoute:
        self.routes[route.id] = route
        return route

    def get_service_by_id(self, service_id: str) -> ServiceEntity | None:
        return self.services.get(service_id)

    def get_service_by_name(self, name: str) -> ServiceEntity | None:
        return next((service for service in self.services.values() if service.name == name), None)

    def list_services(self) -> list[ServiceEntity]:
        return list(self.services.values())

    def list_routes(self, service_id: str) -> list[ApiRoute]:
        return [route for route in self.routes.values() if route.service_id == service_id]

    def list_all_routes(self) -> list[ApiRoute]:
        return list(self.routes.values())

    def delete_service(self, service: ServiceEntity) -> None:
        self.services.pop(service.id, None)

    def save_service(self, service: ServiceEntity) -> ServiceEntity:
        self.services[service.id] = service
        return service


@pytest.fixture
def registry_service() -> ServiceRegistryService:
    return ServiceRegistryService(FakeServiceRepository())


def test_register_service_and_resolve_route(registry_service: ServiceRegistryService) -> None:
    payload = ServiceRegisterRequest(
        name="demo_microservice",
        base_url="http://demo_microservice:8005",
        health_url="http://demo_microservice:8005/health",
        status="ACTIVE",
        version="1.0.0",
        routes=[
            ApiRouteCreateRequest(
                path="/demo/public",
                method="GET",
                is_protected=False,
                required_permission=None,
            )
        ],
    )

    service = registry_service.register_service(payload)
    resolved_service, resolved_route = registry_service.resolve_route("/demo/public", "GET")

    assert service.name == "demo_microservice"
    assert resolved_service.id == service.id
    assert resolved_route.path == "/demo/public"


def test_resolve_route_raises_not_found_for_unknown_route(registry_service: ServiceRegistryService) -> None:
    with pytest.raises(NotFoundException):
        registry_service.resolve_route("/missing", "GET")
