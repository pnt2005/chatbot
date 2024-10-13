from dotenv import load_dotenv
load_dotenv()
import os
from langchain_community.document_loaders import TextLoader # type: ignore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector # type: ignore
from langchain_postgres.vectorstores import PGVector # type: ignore
from langchain.tools.retriever import create_retriever_tool
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver # type: ignore
from langgraph.prebuilt import create_react_agent # type: ignore

loader = TextLoader('doc.txt', encoding='utf-8')
document = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
texts = text_splitter.split_documents(document)

embeddings = OpenAIEmbeddings()

db = PGVector(
    embeddings=embeddings,
    collection_name='doc',
    connection=os.getenv('DATABASE_URL'),
    use_jsonb=True,
)
#db.add_documents(texts)

memory = MemorySaver()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7
)   

retriever = db.as_retriever()

tool = create_retriever_tool(
    retriever,
    "document_retriever",
    "search information from document",
)
tools = [tool]

prompt = """
You are a helpful assistant. First, answer the user's question clearly and concisely.
Then, think of 4 relevant follow-up questions that could deepen or clarify the user's understanding.
"""

agent = create_react_agent(llm, tools, state_modifier=prompt, checkpointer=memory)

config = {"configurable": {"thread_id": "1"}}

def response(query):
    res = agent.invoke({"messages": query}, config=config)
    return res['messages'][-1].content
