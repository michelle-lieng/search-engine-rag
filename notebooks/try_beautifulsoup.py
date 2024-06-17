import requests
from bs4 import BeautifulSoup

# Read bing api key
with open(r'src\BING_api_key.txt') as f:
    bing_api_key = f.read()

# 1. Get search results from Bing API
search_url = "https://api.bing.microsoft.com/v7.0/search"
headers = {"Ocp-Apim-Subscription-Key": bing_api_key}
params = {"q": "python programming", "textDecorations": True, "textFormat": "HTML"}
response = requests.get(search_url, headers=headers, params=params)
search_results = response.json()

# 2. Scrape each result URL
for result in search_results["webPages"]["value"]:
    url = result["url"]
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    
    # 3. Extract text content
    text_content = soup.get_text()
    print(f"Content from {url}:\n{text_content}\n")