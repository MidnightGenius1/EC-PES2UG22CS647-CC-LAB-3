from locust import task, run_single_user
from locust import FastHttpUser
from insert_product import login

class AddToCart(FastHttpUser):
    def __init__(self, environment):
        super().__init__(environment)
        self.username = "test123"
        self.password = "test123"
        self.token = self._get_token()

    def _get_token(self):
        cookies = login(self.username, self.password)
        return cookies.get("token")

    host = "http://localhost:5000"
    default_headers = {
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "DNT": "1",
        "Sec-GPC": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    }

    @task
    def t(self):
        task_headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
            "Cookie": f"token={self.token}",
            "Host": "localhost:5000",
            "Priority": "u=0, i",
            "Referer": "http://localhost:5000/product/1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
        }
        headers = {**self.default_headers, **task_headers}

        with self.client.get("/cart", headers=headers, catch_response=True) as resp:
            if resp.status_code != 200:
                resp.failure(f"Unexpected status code: {resp.status_code}")

if __name__ == "__main__":
    run_single_user(AddToCart)
