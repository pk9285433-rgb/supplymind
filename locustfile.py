from locust import HttpUser, task, between

class SupplyMindUser(HttpUser):
    wait_time = between(1, 2)
    host = "https://supplymind-zmk0.onrender.com"

    @task(3)
    def supplier_details(self):
        self.client.get(
            "/api/analytics/supplier-details?supplier_id=SUP-0001",
            name="supplier_details"
        )

    @task(3)
    def supplier_risks(self):
        self.client.get(
            "/api/analytics/supplier-risks",
            name="supplier_risks"
        )

    @task(2)
    def inventory_summary(self):
        self.client.get(
            "/api/analytics/inventory-summary",
            name="inventory_summary"
        )

    @task(2)
    def forecast_accuracy(self):
        self.client.get(
            "/api/analytics/forecast-accuracy",
            name="forecast_accuracy"
        )

    @task(1)
    def disruption_risks(self):
        self.client.get(
            "/api/analytics/disruption-risks",
            name="disruption_risks"
        )