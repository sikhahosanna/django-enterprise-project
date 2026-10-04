from locust import HttpUser, task, between
import os


class ServiceBookingLoadTest(HttpUser):

    wait_time = between(1, 2)

    def on_start(self):
        self.token = os.getenv("TEST_ACCESS_TOKEN", "")

    def auth_headers(self):
        return {
            "Authorization": f"Bearer {self.token}"
        }

    @task(3)
    def service_search(self):
        self.client.get(
            "/api/v1/services/?search=cleaning",
            headers=self.auth_headers(),
            name="Service Search",
        )

    @task(2)
    def booking(self):
        self.client.get(
            "/api/v1/bookings/",
            headers=self.auth_headers(),
            name="Booking",
        )

    @task(2)
    def booking_history(self):
        self.client.get(
            "/api/v1/rides/optimized-history/",
            headers=self.auth_headers(),
            name="Booking History",
        )

    @task(2)
    def notifications(self):
        self.client.get(
            "/api/v1/notifications/",
            headers=self.auth_headers(),
            name="Notifications",
        )