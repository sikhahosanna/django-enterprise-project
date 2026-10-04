from django.db import IntegrityError

from ..models import SavedService


class SavedServiceService:

    @staticmethod
    def save_service(customer, service):
        try:
            saved_service = SavedService.objects.create(
                customer=customer,
                service=service,
            )
        except IntegrityError:
            raise ValueError(
                "Service is already saved"
            )

        return saved_service

    @staticmethod
    def get_saved_services(customer):
        return SavedService.objects.filter(
            customer=customer
        ).select_related("service").order_by("-created_at")

    @staticmethod
    def delete_saved_service(customer, saved_service):
        if saved_service.customer != customer:
            raise PermissionError(
                "You can only remove your own saved service"
            )

        saved_service.delete()