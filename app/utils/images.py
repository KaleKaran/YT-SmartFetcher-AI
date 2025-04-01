import requests
from duckduckgo_search import DDGS
from pathlib import Path
import os

def determine_diagram_query(summary):
    """
    Determine image search query based on summary content.
    
    Args:
        summary (str): Generated summary text
        
    Returns:
        str: Search query for diagram images
    """
    if "8086" in summary:
        return "8086 microprocessor architecture block diagram"
    else:
        keywords = summary.split()[:5]
        return " ".join(keywords) + " diagram"

def download_relevant_images(search_query):
    """
    Download relevant images for the given search query.
    
    Args:
        search_query (str): Query to search for images
        
    Returns:
        list: List of downloaded image filenames or error message
    """
    try:
        with DDGS() as ddgs:
            image_results = ddgs.images(search_query, max_results=5)
        if not image_results:
            return []

        # Get the base directory
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        temp_dir = Path(os.path.join(base_dir, "temp_images"))
        
        downloaded_images = []
        for index, result in enumerate(image_results[:5]):
            image_url = result["image"]
            try:
                response = requests.get(image_url, stream=True, timeout=10)
                if response.status_code == 200:
                    filename = f"image_{index}.jpg"
                    image_path = temp_dir / filename
                    with open(image_path, "wb") as f:
                        for chunk in response.iter_content(1024):
                            f.write(chunk)
                    downloaded_images.append(filename)
            except Exception as e:
                print(f"Error downloading image {index}: {e}")
                continue

        return downloaded_images
    except Exception as e:
        return f"Error downloading images: {str(e)}" 