# Read bing api key
with open(r'src\BING_api_key.txt') as f:
    bing_api_key = f.read()

from langchain_community.utilities import BingSearchAPIWrapper
search = BingSearchAPIWrapper(bing_search_url= "https://api.bing.microsoft.com/v7.0/search", 
                              bing_subscription_key= bing_api_key,
                              k=5)

# search.run gives a simple query
search.run("What workouts should I do for toned arms?")

# search.results gives metadata
results = search.results("apples", 5)

contexts = [f"Title: {result['title']}\nSnippet: {result['snippet']}" for result in results]
contexts

#---------------------------------------

search = BingSearchAPIWrapper(bing_search_url= "https://api.bing.microsoft.com/v7.0/search", 
                              bing_subscription_key= bing_api_key)
search_results = search.results("What workouts should I do for toned arms?", 5)

for result in search_results:
    snippet = result.get('snippet', '')
    title = result.get('title', '')
    link = result.get('link', '')

    print(f"Title: {title}")
    print(f"Link: {link}")
    print(f"Snippet: {snippet}")
    print("---")

