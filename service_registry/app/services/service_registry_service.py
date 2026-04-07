from service_registry.app.models.api_route import ApiRoute
from service_registry.app.models.service import ServiceEntity
from service_registry.app.repositories.service_repository import ServiceRepository
from service_registry.app.schemas.registry import ServiceRegisterRequest
from shared.exceptions.api import NotFoundException


class ServiceRegistryService:
    """Registry for microservice metadata and routes."""

    def __init__(self, repository: ServiceRepository) -> None:
        self.repository = repository

    def register_service(self, data: ServiceRegisterRequest) -> ServiceEntity:
        service = self.repository.get_service_by_name(data.name)
        if service:
            service.base_url = data.base_url
            service.health_url = data.health_url
            service.status = data.status
            service.version = data.version
            service = self.repository.save_service(service)
        else:
            service = self.repository.create_service(
                ServiceEntity(
                    name=data.name,
                    base_url=data.base_url,
                    health_url=data.health_url,
                    status=data.status,
                    version=data.version,
                )
            )
        for route in data.routes:
            self.repository.create_route(
                ApiRoute(
                    service_id=service.id,
                    path=route.path,
                    method=route.method.upper(),
                    is_protected=route.is_protected,
                    required_permission=route.required_permission,
                )
            )
        return service

    def remove_service(self, service_id: str) -> None:
        service = self.repository.get_service_by_id(service_id)
        if not service:
            raise NotFoundException("Service not found")
        self.repository.delete_service(service)

    def get_service_by_name(self, name: str) -> ServiceEntity:
        service = self.repository.get_service_by_name(name)
        if not service:
            raise NotFoundException("Service not found")
        return service

    def list_services(self) -> list[ServiceEntity]:
        return self.repository.list_services()

    def update_status(self, service_id: str, status: str) -> ServiceEntity:
        service = self.repository.get_service_by_id(service_id)
        if not service:
            raise NotFoundException("Service not found")
        service.status = status
        return self.repository.save_service(service)

    def resolve_route(self, path: str, method: str) -> tuple[ServiceEntity, ApiRoute]:
        normalized_method = method.upper()
        for route in self.repository.list_all_routes():
            if route.path == path and route.method == normalized_method:
                service = self.repository.get_service_by_id(route.service_id)
                if not service:
                    break
                return service, route
        raise NotFoundException("Route not found")
