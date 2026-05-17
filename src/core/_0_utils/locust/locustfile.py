from locust import HttpUser, task


class QuickStartUser(HttpUser):

    def on_start(self):
        response = self.client.post(
            "/v1/auth/login/", data={"email": "admin@admin.com", "password": "123"}
        ).json()
        self.client.headers["Authorization"] = f"Bearer {response['access_token']}"

    @task
    def index(self):
        self.client.get("/")

    @task
    def login(self):
        self.client.get("/v1/auth/login/")
