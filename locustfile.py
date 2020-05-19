from faker import Faker
from locust import HttpLocust, task, between, TaskSet

fake = Faker()


class TariffTaskSet(TaskSet):
    @task(10)
    def view_tariff(self):
        self.client.get("/tariff")

    @task(1)
    def view_tariff_filter(self):
        filter_query = fake.word()
        self.client.get(f"/tariff?q={filter_query}&n=25&p=1", name="/tariff?q=[filter]")

    @task(1)
    def view_api(self):
        self.client.get(f"/api/global-uk-tariff", name="/api/global-uk-tariff")

    @task(1)
    def view_api_filter(self):
        filter_query = fake.word()
        self.client.get(
            f"/api/global-uk-tariff?q={filter_query}",
            name="/api/global-uk-tariff?q=[filter]",
        )

    @task(1)
    def view_xlsx(self):
        self.client.get(
            f"/api/global-uk-tariff.xlsx", name="/api/global-uk-tariff.xlsx"
        )

    @task(1)
    def view_csv(self):
        self.client.get(f"/api/global-uk-tariff.csv", name="/api/global-uk-tariff.csv")


class WebsiteUser(HttpLocust):
    wait_time = between(1, 3)
    task_set = TariffTaskSet
    host = "https://check-future-uk-trade-tariffs.service.gov.uk"
