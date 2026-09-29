from locust import HttpUser, task, between


class RideBookingUser(HttpUser):

    wait_time = between(1, 2)

    def on_start(self):
        self.token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzg4MzgzMzc3LCJpYXQiOjE3ODgzODE1NzcsImp0aSI6ImZjYTJhNzBjZjlmYzQ1NzdiZmJlOWIzOWQ1YmMzZTk5IiwidXNlcl9pZCI6IjkzMWVlYTdlLTdjMGYtNGUwNy1iNWI3LTIwNzI3NzZiOWFmNCJ9.oTA3PpRYM9D7hxpgdw-abmLoIlzVPeQ-_L-YHsIhPeI"

    @task
    def nearby_drivers(self):
        self.client.get(
            "/api/v1/drivers/nearby/"
            "?latitude=17.3850"
            "&longitude=78.4867"
            "&radius=10",
            headers={
                "Authorization": f"Bearer {self.token}"
            }
        )