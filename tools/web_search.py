#tools/web_search.py
import urllib.parse
# web search
def web_search(query):
    proper_query = urllib.parse.quote(query)
    url = f"https://duckduckgo.com/?q={proper_query}"
    return f" WEB RESULT : {url}"