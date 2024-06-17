from sklearn.feature_extraction.text import TfidfVectorizer
import faiss
from src.webcrawler import run_spider
from src.chatbot_setup import get_bing_search_results, system_prompt, chunk_clean, search
from openai import OpenAI
import json # for readability of the chat history

# Read openai key
with open(r'src\GPT_api_key.txt') as f:
    openai_api_key = f.read()

# Function for chatbot
def conversation():
    user_query = ""  # Initialize x with an empty string
    chat_history = [] # Define chat history

    while True:
        user_query = input("Ask anything: ")

        if user_query.lower() == "end":
            break
        else:
            urls = get_bing_search_results(user_query)
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

            # Perform similarity search - retrieve 5 similarity documents to user query
            relevant_chunks = search(user_query, vectorizer, index, df=chunked_df, top_n=5)

            #initialize system prompt to be added to the model
            system = {"role": "system", "content": system_prompt.format(website_extract=relevant_chunks)}

            # add in user_query to chat history 
            chat_history.append({"role": "user", "content": user_query})

            # call openai api
            client = OpenAI(api_key=openai_api_key)

            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[system] + chat_history,
                temperature=0,
                #max_tokens=200,
                frequency_penalty=0
            )

            chatbot_response = completion.choices[0].message.content
            chat_history.append({"role": "assistant", "content": chatbot_response})
            
            print("\n")
            print("This is the pdf extracts: ")
            print("-------------------------")
            for line in relevant_chunks:
                print(line)
                print("\n")
            print("This is the chatbot response: ")
            print("-----------------------------")
            print(chatbot_response)
            print("\n")
            print("This is the chat history: ")
            print("-------------------------")
            for entry in chat_history:
                print(json.dumps(entry, indent=4))
            print("\n")
            print("This is the token count: ")
            print("-------------------------")
            print(f'{completion.usage.prompt_tokens} prompt tokens counted by the OpenAI API.')
            print(f'You have {4097 - completion.usage.prompt_tokens} remaining tokens for the gpt-3.5-turbo model.')
            print("\n")
            continue

# run function
conversation()