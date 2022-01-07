import faker
from locust import HttpUser, task, between

fake = faker.Faker()


class InventoryUser(HttpUser):

    host = 'https://api.latihan.jocki.me'
    access_token = None
    wait_time = between(1, 5)

    def on_start(self):
        response = self.client.post(
            'https://auth.latihan.jocki.me/auth/realms/latihan/protocol/openid-connect/token',
            headers={
                'Authorization': 'Basic bG9jdXN0OmxvY3VzdA==',
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data={
                'grant_type': 'urn:ietf:params:oauth:grant-type:uma-ticket',
                'audience': 'locust',
            }
        )
        self.access_token = response.json()['access_token']

    @task
    def create_item(self):
        self.client.post(
            '/stock-item-service/items',
            headers={
                'Authorization': 'Bearer ' + self.access_token
            },
            json={
                "sku": fake.bothify(text="???-#####"),
                "name": fake.name(),
                "quantity": fake.random_int(),
                "category": fake.random_element(('CPU', 'Memory', 'Storage', 'Motherboard', 'GPU'))
            }
        )
