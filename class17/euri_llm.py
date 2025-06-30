import requests

def euri_completion(messages, temperature=0.7, max_tokens=1000):
    url = "https://api.euron.one/api/v1/euri/alpha/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiJhNTM3YzM3Zi0xNmFkLTRjZTUtYjRhMC0wNTNjYTIyNzE1YTgiLCJlbWFpbCI6InN1ZGhhbnNodUBldXJvbi5vbmUiLCJpYXQiOjE3NDMyMzkyNTYsImV4cCI6MTc3NDc3NTI1Nn0.HRHeCucOK0hPVZQwyvNoD0GaHarvHNivjJ2l6-xU1HA"
    }
    payload = {
        "messages": messages,
        "model": "gpt-4.1-nano",
        "max_tokens": max_tokens,
        "temperature": temperature
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()["choices"][0]["message"]["content"]
