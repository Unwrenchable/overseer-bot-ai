import requests

class RealAIClient:
    def __init__(self, base_url="http://localhost:8000", api_key=None):
        self.base_url = base_url
        self.headers = {"x-api-key": api_key} if api_key else {}

    def chat(self, prompt: str):
        resp = requests.post(f"{self.base_url}/chat", json={"prompt": prompt}, headers=self.headers)
        return resp.json()

    def generate_quest(self, npc_name: str):
        resp = requests.post(f"{self.base_url}/quest", json={"npc_name": npc_name}, headers=self.headers)
        return resp.json()

    def post_tweet(self, text: str, image_path=None):
        resp = requests.post(
            f"{self.base_url}/twitter/post",
            json={"text": text, "image_path": image_path},
            headers=self.headers
        )
        return resp.json()

# Usage example:
# client = RealAIClient(api_key="your-key")
# print(client.generate_quest("Overseer"))
