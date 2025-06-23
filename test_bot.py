from langchain_openai import ChatOpenAI
import os

os.environ["OPENAI_API_KEY"] = "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"

llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
response = llm.invoke("Give me 3 strategies for teaching reading comprehension.")
print(response.content)

