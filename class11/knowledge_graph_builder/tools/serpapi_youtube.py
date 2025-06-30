# SerpAPI YouTube search integration
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Get SerpAPI key from environment variables
SERP_API_KEY = os.getenv('SERPAPI_API_KEY')

def search_youtube_serpapi(query, max_results=5):
    """
    Search for YouTube videos using SerpAPI's YouTube engine
    
    Args:
        query: The search query for YouTube videos
        max_results: Maximum number of results to return (default: 5)
        
    Returns:
        List of video information dictionaries
    """

    
    try:
        # Construct the SerpAPI YouTube search URL
        url = "https://serpapi.com/search.json"
        params = {
            "engine": "youtube",  # Use YouTube search engine
            "search_query": query,  # The search term
            "api_key": SERP_API_KEY,
            "hl": "en",  # Language for search results
            "gl": "us"   # Country for search results
        }
        
        # Make the request to SerpAPI
        response = requests.get(url, params=params)
        data = response.json()
        
        # Process the results
        results = []
        
        # SerpAPI returns video results in the 'video_results' field
        video_results = data.get('video_results', [])
        
        for item in video_results[:max_results]:
            # Extract thumbnail URL - SerpAPI provides both static and rich thumbnails
            thumbnail_url = ''
            if 'thumbnail' in item:
                if isinstance(item['thumbnail'], dict):
                    thumbnail_url = item['thumbnail'].get('static', '')
                else:
                    thumbnail_url = item['thumbnail']
            
            # Create a standardized result object
            result = {
                'title': item.get('title', ''),
                'link': item.get('link', ''),
                'description': item.get('snippet', ''),
                'thumbnail': thumbnail_url,
                'channel': item.get('channel', {}).get('name', '') if isinstance(item.get('channel'), dict) else '',
                'views': item.get('views', ''),
                'published': item.get('published_date', ''),
                'duration': item.get('length', '')
            }
            results.append(result)
        
        # If no video results found but there are other types of results
        if not video_results and 'organic_results' in data:
            for item in data.get('organic_results', [])[:max_results]:
                result = {
                    'title': item.get('title', ''),
                    'link': item.get('link', ''),
                    'description': item.get('snippet', ''),
                    'thumbnail': '',  # Organic results might not have thumbnails
                    'channel': '',
                    'views': '',
                    'published': '',
                    'duration': ''
                }
                results.append(result)
            
        return results
    
    except Exception as e:
        return [{
            'title': f'Error searching YouTube via SerpAPI: {str(e)}',
            'link': '',
            'description': ''
        }]


# Example usage
if __name__ == "__main__":
    print("\n=== Testing SerpAPI YouTube Search ===\n")
    
    # Test with an educational query
    query = "machine learning tutorial"
    print(f"Searching for: '{query}'\n")
    
    results = search_youtube_serpapi(query)
    
    if results and results[0].get('title', '').startswith('Error'):
        print(f"Error: {results[0]['title']}")
    else:
        print(f"Found {len(results)} results:\n")
        
        for i, result in enumerate(results, 1):
            print(f"Result {i}:")
            print(f"Title: {result['title']}")
            print(f"Link: {result['link']}")
            print(f"Channel: {result['channel']}")
            print(f"Description: {result['description'][:100]}..." if result['description'] else "Description: N/A")
            print(f"Thumbnail: {result['thumbnail']}")
            print(f"Views: {result['views']}")
            print(f"Duration: {result['duration']}")
            print(f"Published: {result['published']}")
            print("---\n")
            
    print("To use this in your code:")
    print("from tools.serpapi_youtube import search_youtube_serpapi")
    print("results = search_youtube_serpapi('your search query')")
    print("\nNote: This requires a valid SERPAPI_API_KEY in your .env file")