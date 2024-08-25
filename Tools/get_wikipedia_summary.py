from .tool import Tool
from .tool_registry import ToolRegistry
import requests

def get_wikipedia_summary(page_title: str) -> str:
    try:
        url = "https://en.wikipedia.org/w/api.php"
        params = {
            'action': 'query',
            'format': 'json',
            'titles': page_title,
            'prop': 'extracts',
            'exintro': True,
            'explaintext': True,
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        
        data = response.json()
        page = next(iter(data['query']['pages'].values()))
        
        if 'extract' in page:
            return page['extract']
        elif 'missing' in page:
            return f"Error: The page '{page_title}' does not exist on Wikipedia."
        else:
            return f"No summary available for '{page_title}'."
    
    except requests.exceptions.Timeout:
        return f"Error: Request timed out while fetching summary for '{page_title}'."
    except requests.exceptions.HTTPError as e:
        return f"Error: HTTP error occurred while fetching summary for '{page_title}': {str(e)}"
    except requests.exceptions.RequestException as e:
        return f"Error: An unexpected error occurred while fetching summary for '{page_title}': {str(e)}"
    except Exception as e:
        return f"Error: An unexpected error occurred: {str(e)}"

def register(registry: ToolRegistry):
    registry.register_tool(Tool(
        name="get_wikipedia_summary",
        description="Retrieves a summary of a Wikipedia page for a given title. It returns the introductory section of the Wikipedia article. This tool is useful for getting quick, factual information about a topic. It handles errors for non-existent pages, network issues, and other potential problems. The summary is limited to the intro section and may not contain all details from the full article.",
        function=get_wikipedia_summary,
        input_schema={
            "type": "object",
            "properties": {
                "page_title": {
                    "type": "string",
                    "description": "The title of the Wikipedia page to summarize. This should be the exact title as it appears on Wikipedia."
                }
            },
            "required": ["page_title"]
        }
    ))