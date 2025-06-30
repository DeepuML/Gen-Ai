# SERPAPI integration
import os
from dotenv import load_dotenv
load_dotenv()
import requests
# Initialize SerpAPI with the API key from environment variables 

SERP_API_KEY = os.getenv('SERPAPI_API_KEY')

def search_google(query):
    url=f"https://serpapi.com/search.json?q={query}&api_key={os.getenv('SERPAPI_API_KEY')}"
    response = requests.get(url).json().get('organic_results', [])
    results = []
    
    # Process the top 5 results
    for item in response[:5]:
        results.append({
            'title': item.get('title', ''),
            'link': item.get('link', ''),
            'snippet': item.get('snippet', '')
        })
    
    return results