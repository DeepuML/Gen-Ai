import os
import json
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get YouTube API key from environment variables
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")


class YouTubeSearchTool:
    """Tool for searching YouTube videos using the YouTube Data API."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the YouTube search tool with an API key."""
        self.api_key = api_key or YOUTUBE_API_KEY
        if not self.api_key:
            print("Warning: YouTube API key not found. Using simulated results.")

    def search_videos(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """Search for YouTube videos related to the query.
        
        Args:
            query: The search query
            max_results: Maximum number of results to return
            
        Returns:
            List of video information dictionaries
        """
        # If API key is not available, return simulated results
        if not self.api_key:
            return self._get_simulated_results(query, max_results)

        # In a real implementation, this would use the YouTube Data API
        # For now, we'll use simulated results
        return self._get_simulated_results(query, max_results)

    def _get_simulated_results(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Generate simulated YouTube search results for demonstration purposes."""
        # Create a deterministic but varied set of results based on the query
        query_hash = sum(ord(c) for c in query) % 100
        
        # Base templates for video results
        templates = [
            {"title": f"Complete {query} Tutorial for Beginners", "channel": "LearnTech Academy", "views": "1.2M", "duration": "45:22", "published": "2 months ago"},
            {"title": f"Advanced {query} Techniques", "channel": "CodeMaster Pro", "views": "890K", "duration": "32:15", "published": "5 months ago"},
            {"title": f"{query} Crash Course 2023", "channel": "Quick Learner", "views": "2.5M", "duration": "1:22:45", "published": "3 weeks ago"},
            {"title": f"Understanding {query} - Explained Simply", "channel": "Simple Explanations", "views": "1.8M", "duration": "18:30", "published": "1 year ago"},
            {"title": f"Deep Dive into {query} Concepts", "channel": "Tech Insights", "views": "500K", "duration": "55:00", "published": "6 months ago"},
            {"title": f"{query} for Data Science", "channel": "DataDriven", "views": "1.1M", "duration": "28:00", "published": "4 months ago"}
            {"title": f"Practical {query} Projects for Portfolio", "channel": "Project Builder", "views": "750K", "duration": "55:10", "published": "4 months ago"},
            {"title": f"{query} for Absolute Beginners", "channel": "Beginner Friendly", "views": "3.1M", "duration": "28:45", "published": "8 months ago"},
            {"title": f"Master {query} in 30 Days", "channel": "Coding Challenge", "views": "1.5M", "duration": "15:20", "published": "2 years ago"},
            {"title": f"What's New in {query} 2023", "channel": "Tech Updates", "views": "980K", "duration": "42:18", "published": "1 month ago"},
            {"title": f"{query} Best Practices and Tips", "channel": "Code Optimizer", "views": "1.1M", "duration": "37:55", "published": "6 months ago"},
            {"title": f"How I Learned {query} in One Week", "channel": "Fast Learner", "views": "2.2M", "duration": "25:40", "published": "3 months ago"},
        ]
        
        # Generate results with video IDs and thumbnails
        results = []
        for i in range(min(max_results, len(templates))):
            template = templates[(i + query_hash) % len(templates)]
            video_id = f"yt{query_hash}{i}".replace(" ", "")[:11]
            
            result = {
                "id": video_id,
                "title": template["title"],
                "channel": template["channel"],
                "description": f"Learn all about {query} in this comprehensive video. Perfect for all skill levels.",
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "thumbnail": f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg",
                "views": template["views"],
                "duration": template["duration"],
                "published": template["published"]
            }
            results.append(result)
            
        return results


# Example usage
if __name__ == "__main__":
    youtube_tool = YouTubeSearchTool()
    results = youtube_tool.search_videos("Python programming")
    print(json.dumps(results, indent=2))