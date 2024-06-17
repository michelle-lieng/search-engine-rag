
import requests

def scrape_jina_ai(url: str) -> str:
  response = requests.get("https://r.jina.ai/" + url)
  return response.text

url = "https://en.wikipedia.org/wiki/Dog"

print(scrape_jina_ai(url))


"""
def scrape_jina_ai(url: str) -> str:
  response = requests.get("https://r.jina.ai/" + url)
  return response.text

data = pd.DataFrame(columns=["url","context"])

for url in urls[0]:
    new_row = pd.DataFrame({'url': url, "context":scrape_jina_ai(url)}, index=['NewRow'])
    data = pd.concat([data, new_row], ignore_index=True)

for url in urls[0]:
    scrape_jina_ai(url)

"""