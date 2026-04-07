from sqlalchemy import select
from sqlalchemy.orm import Session

from service_registry.app.models.api_route import ApiRoute
from service_registry.app.models.service import ServiceEntity


class ServiceRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create_service(self, service: ServiceEntity) -> ServiceEntity:
        self.session.add(service)
        self.session.commit()
        self.session.refresh(service)
        return service

    def create_route(self, route: ApiRoute) -> ApiRoute:
        self.session.add(route)
        self.session.commit()
        self.session.refresh(route)
        return route

    def get_service_by_id(self, service_id: str) -> ServiceEntity | None:
        return self.session.get(ServiceEntity, service_id)

    def get_service_by_name(self, name: str) -> ServiceEntity | None:
        return self.session.execute(select(ServiceEntity).where(ServiceEntity.name == name)).scalar_one_or_none()

    def list_services(self) -> list[ServiceEntity]:
        return list(self.session.execute(select(ServiceEntity).order_by(ServiceEntity.created_at.desc())).scalars().all())

    def list_routes(self, service_id: str) -> list[ApiRoute]:
        return list(self.session.execute(select(ApiRoute).where(ApiRoute.service_id == service_id)).scalars().all())

    def list_all_routes(self) -> list[ApiRoute]:
        return list(self.session.execute(select(ApiRoute)).scalars().all())

    def delete_service(self, service: ServiceEntity) -> None:
        for route in self.list_routes(service.id):
            self.session.delete(route)
        self.session.delete(service)
        self.session.commit()

    def save_service(self, service: ServiceEntity) -> ServiceEntity:
        self.session.add(service)
        self.session.commit()
        self.session.refresh(service)
        return service
