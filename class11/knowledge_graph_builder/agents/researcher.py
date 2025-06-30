# Researcher agent logic here
from knowledge_graph_builder.tools.serpapi_tool import search_google
from knowledge_graph_builder.tools.wikipedia_tool import search_wikipedia
from knowledge_graph_builder.tools.serpapi_youtube import search_youtube_serpapi
import requests
import os
from dotenv import load_dotenv
# Note: serpapi_youtube is imported dynamically in the search_youtube_serpapi function to avoid circular imports

load_dotenv()

def search_youtube(query, max_results=8):
    """Search for educational videos and courses on YouTube"""
    api_key = os.getenv('YOUTUBE_API_KEY', '')
    if not api_key:
        return [{
            'title': 'YouTube API key not configured',
            'link': '',
            'description': 'Please add YOUTUBE_API_KEY to your .env file'
        }]
    
    try:
        url = f"https://www.googleapis.com/youtube/v3/search"
        params = {
            'part': 'snippet',
            'q': query + ' full course tutorial',  # Emphasize full courses
            'type': 'video',
            'maxResults': max_results,
            'key': api_key,
            'relevanceLanguage': 'en',
            'videoEmbeddable': 'true',
            'videoDuration': 'long',  # Prefer longer videos for courses (>20 mins)
            'order': 'relevance'
        }
        response = requests.get(url, params=params)
        data = response.json()
        
        results = []
        for item in data.get('items', []):
            video_id = item.get('id', {}).get('videoId', '')
            snippet = item.get('snippet', {})
            results.append({
                'title': snippet.get('title', ''),
                'link': f"https://www.youtube.com/watch?v={video_id}",
                'description': snippet.get('description', ''),
                'thumbnail': snippet.get('thumbnails', {}).get('high', {}).get('url', '')
            })
        return results
    except Exception as e:
        return [{'title': f'Error searching YouTube: {str(e)}', 'link': '', 'description': ''}]

def search_online_courses(topic):
    """Search for online courses from platforms like Coursera, Udemy, edX"""
    # Simulate course search results since we don't have direct API access
    # In a production environment, you would integrate with course platform APIs
    platforms = [
        {
            'name': 'Coursera',
            'url': f'https://www.coursera.org/search?query={topic}',
            'courses': [
                {'title': f'{topic} Specialization', 'level': 'Beginner to Intermediate'},
                {'title': f'Introduction to {topic}', 'level': 'Beginner'}
            ]
        },
        {
            'name': 'Udemy',
            'url': f'https://www.udemy.com/courses/search/?q={topic}',
            'courses': [
                {'title': f'Complete {topic} Bootcamp', 'level': 'All Levels'},
                {'title': f'Advanced {topic} Masterclass', 'level': 'Advanced'}
            ]
        },
        {
            'name': 'edX',
            'url': f'https://www.edx.org/search?q={topic}',
            'courses': [
                {'title': f'{topic} Professional Certificate', 'level': 'Intermediate'},
                {'title': f'{topic} Fundamentals', 'level': 'Beginner'}
            ]
        }
    ]
    return platforms

def search_books(topic):
    """Search for relevant books on the topic"""
    try:
        # Google Books API doesn't require an API key for basic searches
        url = "https://www.googleapis.com/books/v1/volumes"
        params = {
            'q': f'{topic} textbook OR guide OR handbook',
            'maxResults': 5,
            'orderBy': 'relevance',
            'printType': 'books'
        }
        response = requests.get(url, params=params)
        data = response.json()
        
        books = []
        for item in data.get('items', []):
            volume_info = item.get('volumeInfo', {})
            # Get book cover image URL
            image_links = volume_info.get('imageLinks', {})
            thumbnail = image_links.get('thumbnail', '') or image_links.get('smallThumbnail', '')
            
            books.append({
                'title': volume_info.get('title', ''),
                'authors': volume_info.get('authors', []),
                'publisher': volume_info.get('publisher', ''),
                'publishedDate': volume_info.get('publishedDate', ''),
                'description': volume_info.get('description', '')[:200] + '...' if volume_info.get('description') else '',
                'link': volume_info.get('infoLink', ''),
                'cover_image': thumbnail
            })
        return books
    except Exception as e:
        return [{'title': f'Error searching books: {str(e)}', 'authors': []}]

def search_youtube_serpapi(query):
    """Search for educational videos on YouTube using SerpAPI"""
    # Import here to avoid circular imports
    try:
        from knowledge_graph_builder.tools.serpapi_youtube import search_youtube_serpapi as serpapi_youtube_search
        return serpapi_youtube_search(query)
    except Exception as e:
        print(f"Error using SerpAPI YouTube search: {str(e)}")
        return [{
            'title': f"Error using SerpAPI YouTube search: {str(e)}", 
            'link': "", 
            'channel': "", 
            'description': "Please check your SerpAPI key and internet connection.", 
            'thumbnail': "", 
            'views': "", 
            'duration': "", 
            'published': ""
        }]

def search_youtube_courses(topic):
    """Search specifically for courses on YouTube"""
    # Use a more specific query for finding courses
    course_query = f"{topic} complete course certification"
    return search_youtube(course_query, max_results=10)

def run_researcher(topic, use_serpapi_youtube=False):
    # Append "learning resources" to make the search more education-focused
    education_topic = f"{topic} learning resources"
    
    # Run searches
    google_results = search_google(education_topic)
    wiki_summary = search_wikipedia(topic)
    
    # Use SerpAPI YouTube search if specified, otherwise use regular YouTube API
    if use_serpapi_youtube:
        youtube_results = search_youtube_serpapi(topic)
        youtube_courses = search_youtube_serpapi(f"{topic} complete course")
    else:
        youtube_results = search_youtube(topic)
        youtube_courses = search_youtube_courses(topic)
    
    online_courses = search_online_courses(topic)
    book_recommendations = search_books(topic)
    
    return {
        "google": google_results,
        "wiki": wiki_summary,
        "youtube": youtube_results,
        "youtube_courses": youtube_courses,
        "courses": online_courses,
        "books": book_recommendations
    }

# Example usage
if __name__ == "__main__":
    topic = "Artificial Intelligence"
    research_results = run_researcher(topic)
    print("Google Results:", research_results["google"])
    print("Wikipedia Summary:", research_results["wiki"])