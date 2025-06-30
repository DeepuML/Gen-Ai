import requests
from crewai.llm import BaseLLM

class EuriLLM(BaseLLM):
    def __init__(self, model="gpt-4.1-nano"):
        super().__init__(model=model)

    def call(self, prompt: str, **kwargs) -> str:
        print("\n🔍 EURI Prompt:\n", prompt[:300])
        try:
            response = requests.post(
                "https://api.euron.one/api/v1/euri/alpha/chat/completions",
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": kwargs.get("temperature", 0.7),
                    "max_tokens": kwargs.get("max_tokens", 1024)
                },
                headers={
                    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiJhNjk1YzBmMS0xMzZkLTQwNzgtYjY3Ni02MWIwMzM5YzU5YTkiLCJlbWFpbCI6Im1haGFrYWwxMjMzMjFAZ21haWwuY29tIiwiaWF0IjoxNzQ5OTc2ODg4LCJleHAiOjE3ODE1MTI4ODh9.lSiE86P3RPE9p8ofXst0dNLjvb8ivnWqLbsNl9J1dLg",
                    "Content-Type": "application/json"
                }
            )

            if response.status_code != 200:
                raise Exception(f"API Error: {response.status_code} - {response.text}")

            return response.json()["choices"][0]["message"]["content"].strip()

        except Exception as e:
            raise Exception(f"[EuriLLM Error] {str(e)}")
