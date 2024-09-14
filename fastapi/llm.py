from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

llm = ChatOpenAI(
    model="gpt-3.5-turbo-1106",
    temperature=0.7
)

conversation = ConversationChain(
        llm=llm,
        verbose=True,
        memory=ConversationBufferMemory()
)

def response(text):
    conversation.predict(input = text)
    return conversation.memory.buffer_as_messages[-1].content