import requests
import pandas as pd
import json
import spacy

# Read bing api key
with open(r'src\BING_api_key.txt') as f:
    bing_api_key = f.read()

def get_bing_search_results(query):
    subscription_key = bing_api_key
    search_url = "https://api.bing.microsoft.com/v7.0/search"
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    params = {"q": query, "textDecorations": True, "textFormat": "HTML"}
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
    return [result['url'] for result in search_results.get('webPages', {}).get('value', [])]

system_prompt = """
You are a helpful Assistant who answers users' questions based on multiple contexts given to you.
Keep your answer detailed and ensure you are answering the query.
The evidence is the context of a website extract with metadata of its URL.
Make sure to add the exact 'url' at the end of the sentence you are citing to.
Use multiple sources and provide citations for each piece of information you include in the answer.
Reply "Not applicable" if the text is irrelevant.
Ensure your response is formatted with citations in the format: (Author, Year).
Include a "Sources:" section at the end with full references.
The website content is: {website_extract}
"""

def chunk_clean():
    # Read the file as a string
    with open(r'scraped_data.json', 'r', encoding='utf-8') as file:
        data = file.read()

    # Check if the string contains multiple lists
    if '][' in data:
        # Correct the format by adding commas between the lists
        data = data.replace('][', '],[')
        # Wrap the entire string in square brackets to form a valid JSON array
        data = f'[{data}]'
        # Load the corrected JSON string
        data = json.loads(data)[-1]
    else:
        data = json.loads(data)

    # Convert the last list to a DataFrame
    data = pd.DataFrame(data)

    # Load spaCy model
    nlp = spacy.load('en_core_web_sm')

    def clean_text(text):
        # Remove newlines
        text = text.replace('\n', ' ').replace('\r', ' ')
        # Process text with spaCy
        doc = nlp(text)
        # Remove stopwords and punctuation, and lemmatize
        tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
        return ' '.join(tokens)

    def chunk_text(text, chunk_size=150, overlap=30):
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size - overlap):
            chunks.append(' '.join(words[i:i + chunk_size]))
        return chunks

    # Clean and chunk the content with overlap
    all_chunks = []
    for _, row in data.iterrows():
        clean_content = clean_text(row['content'])
        chunks = chunk_text(clean_content)
        for chunk in chunks:
            all_chunks.append({'url': row['url'], 'content_chunk': chunk})

    # Convert chunked data to DataFrame
    chunked_df = pd.DataFrame(all_chunks)
    return chunked_df

# Define search function
def search(query, vectorizer, index, df, top_n=5):
    query_vector = vectorizer.transform([query]).toarray().astype('float32')
    D, I = index.search(query_vector, top_n)
    results = df.iloc[I[0]].to_dict(orient='records')
    return results