from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

model = ChatOpenAI(
    model="gpt-3.5-turbo-1106",
    temperature=0.7
)

def response(text):
    prompt = ChatPromptTemplate.from_messages([
        ("human", "{input}")
    ])

    parser = StrOutputParser()
    chain = prompt | model | parser

    return chain.invoke({
        "input": text
    })

