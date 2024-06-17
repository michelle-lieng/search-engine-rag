import requests
from notebooks.crawler_function import run_spider

# Read bing api key
with open(r'src\BING_api_key.txt') as f:
    bing_api_key = f.read()

# Step 1: Query the Bing API
# outputs a bunch of urls 
def get_bing_search_results(query):
    subscription_key = bing_api_key
    search_url = "https://api.bing.microsoft.com/v7.0/search"
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    params = {"q": query, "textDecorations": True, "textFormat": "HTML"}
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
    return [result['url'] for result in search_results.get('webPages', {}).get('value', [])]

urls = get_bing_search_results("What is the impact of climate change on agriculture?")

# Scrape content from URLs using Scrapy
run_spider(urls)
