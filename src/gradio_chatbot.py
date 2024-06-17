from sklearn.feature_extraction.text import TfidfVectorizer
import faiss
from src.webcrawler import run_spider
from src.chatbot_setup import get_bing_search_results, system_prompt, chunk_clean, search
from openai import OpenAI
import gradio as gr

# Read openai key
with open(r'src\GPT_api_key.txt') as f:
    openai_api_key = f.read()

#message = "What is the impact of climate change on agriculture?"

# Create function for gradio chatbot
def gradio_chatbot(message: str, history: list) -> str:

    urls = get_bing_search_results(message)
    run_spider(urls)

    chunked_df = chunk_clean()

    # Convert text to vectors using TfidfVectorizer
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(chunked_df['content_chunk'])
    # Convert sparse matrix to dense
    X_dense = X.toarray().astype('float32')
    # Create FAISS index
    index = faiss.IndexFlatL2(X_dense.shape[1])  # L2 distance
    index.add(X_dense)

    # Perform similarity search
    relevant_chunks = search(message, vectorizer, index, df=chunked_df, top_n=5)

    #initialize system prompt to be added to the model
    system = {"role": "system", "content": system_prompt.format(website_extract=relevant_chunks)}

    history_openai_format = []
    for human, assistant in history:
        history_openai_format.append({"role": "user", "content": human })
        history_openai_format.append({"role": "assistant", "content":assistant})
    history_openai_format.append({"role": "user", "content": message})
    
    # Initialize the OpenAI client
    client = OpenAI(api_key=openai_api_key)

    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[system] + history_openai_format,
        #max_tokens=200,
        temperature=0,
        frequency_penalty=0,
        stream=True,
    )
    partial_message = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            partial_message = partial_message + chunk.choices[0].delta.content
            yield partial_message
            
gr.ChatInterface(
    gradio_chatbot, 
    chatbot=gr.Chatbot(height=300),
    textbox=gr.Textbox(placeholder="Ask me a question", container=False, scale=7),
    title="Qiri",
    description="Ask Qiri any question!",
    theme="soft",
    examples=["What is the impact of climate change on agriculture?"],
    cache_examples=True,
    retry_btn=None,
    undo_btn="Delete Previous",
    clear_btn="Clear",
).launch()