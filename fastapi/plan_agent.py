from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from typing import List
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage, ToolMessage
from pydantic import BaseModel

#define model and graph
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7,
)

class State(TypedDict):
    messages: Annotated[list, add_messages]

graph = StateGraph(State)

#get info node
get_info_template = """Your job is to get information from a user about their travel.
You should get the following information from them:
- Where they want to go
- What transportation they want to go by
- When they want to go
- Who they want to go with
If you are not able to discern this info, ask them to clarify! Do not attempt to wildly guess.
After you are able to discern all the information, call the relevant tool."""

def get_info_prompt(messages):
    return [SystemMessage(content=get_info_template)] + messages

class Info(BaseModel):
    """Information about the user travel"""
    place: str
    transportation: str
    date: str
    member: List[str]

llm_with_tools = llm.bind_tools([Info])

@graph.add_node
def get_info(state: State):
    messages = get_info_prompt(state["messages"])
    response = llm_with_tools.invoke(messages)
    return {"messages": response}

#make plan node
make_plan_template = """Based on the following requirements, write a simple plan for travel:
{reqs}"""

def make_plan_prompt(messages: list):
    for m in messages:
        if isinstance(m, AIMessage) and m.tool_calls:
            return [SystemMessage(content=make_plan_template.format(reqs=m.tool_calls[0]["args"]))]

@graph.add_node
def make_plan(state: State):
    messages = make_plan_prompt(state["messages"])
    response = llm.invoke(messages)
    return {"messages": response}

#tool message node
@graph.add_node
def tool_message(state: State):
    response = [ToolMessage(content='done', tool_call_id=state["messages"][-1].tool_calls[0]["id"])]
    return {"messages": response}

#conditional edges
def get_state(state: State):
    messages = state["messages"]
    if isinstance(messages[-1], AIMessage) and messages[-1].tool_calls:
        return "tool_message"
    return END

#add edges
graph.add_conditional_edges("get_info", get_state, ["tool_message", END])
graph.add_edge("tool_message", "make_plan")
graph.add_edge("make_plan", END)
graph.add_edge(START, "get_info")

#define agent
agent = graph.compile(checkpointer=MemorySaver())

config = {"configurable": {"thread_id": "1"}}

def response(query):
    res = agent.invoke({"messages": query}, config=config)
    return res['messages'][-1].content

