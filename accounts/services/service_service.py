
from ..models import Service, ServiceImage


class ServiceService:

    @staticmethod
    def get_service(service_id):
        return Service.objects.get(id=service_id)

    @staticmethod
    def get_service_images(service):
        return ServiceImage.objects.filter(
            service=service
        ).order_by("created_at")

    @staticmethod
    def get_service_image(image_id):
        return ServiceImage.objects.get(id=image_id)
