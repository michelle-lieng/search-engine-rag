from langchain.prompts import PromptTemplate

from langchain.llms import OpenAI

with open(r"GPT_api_key.txt") as f:
    openai_api_key = f.read()

class OpenAILLM:
    def __init__(self, openai_api_key=openai_api_key, temperature=0.9, model_name="gpt-3.5-turbo-instruct", max_tokens=200, frequency_penalty=0):
        self.openai_api_key = openai_api_key
        self.temperature = temperature
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.frequency_penalty = frequency_penalty

        self.template = """
        Answer the question based on the context below. If the
        question cannot be answered using the information provided answer
        with "I don't know". Think step by step.

        Context: {context}

        Question: {question}

        Answer: """

        self.prompt = PromptTemplate(input_variables=["context", "question"], template=self.template)

    def llm_call(self, context, question):
        llm = OpenAI(temperature=self.temperature,
                     openai_api_key=self.openai_api_key,
                     model_name=self.model_name,
                     max_tokens=self.max_tokens,
                     frequency_penalty=self.frequency_penalty)

        llm_chain = self.prompt | llm

        return llm_chain.invoke({"context": context, "question": question})

# Example usage
openai_llm = OpenAILLM()

context = "The species called Manipees are blue."
question = "What colour are the species called Manipees?"
#question = "What NFL team won the Super Bowl in the year Justin Bieber was born?"

result = openai_llm.llm_call(context, question)
print(result)