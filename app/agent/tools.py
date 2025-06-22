
import pandas as pd
import requests
import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import tools_condition, ToolNode

load_dotenv()

GROQ_API_KEY = os.environ["GROQ_API_KEY"]
OPENWEATHER_API = os.environ["OPENWEATHER_API"]

message = """""
You are a helpful assistant with a set of different tools.
Depending on the users request you will need to use an specific tool and return
an answer.
Avoid using formats with numbers and using phrases like:
'The answer is', 'The result is'.

"""
sys_message = SystemMessage(content=message)



@tool
def sum(num1: int, num2: int) -> int:
    """"Returns the result of the sum between num1 and num2
    Args:
        num1: int
        num2: int
    """
    return num1 + num2

@tool
def get_city_weather(city: str) -> str:
    """Returns the current weather ona a specific city
    Args:
        city: string
    """
    try:
        api_key = OPENWEATHER_API
        if(api_key is None):
            return "There was an error getting weather API key"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        resp = requests.get(url)
        data = resp.json()
        temperature = data["main"]["temp"]
        description = data["weather"][0]["description"]
        return f"The weather in {city} is {temperature} and {description}"
    except Exception as ex:
        print(ex)




tools = [
    sum,
    get_city_weather
]


def build_graph(provider: str = "groq"):
    """"Build the graph"""

    if provider == 'groq':
        llm = ChatGroq(model="qwen-qwq-32b",
                       api_key=GROQ_API_KEY, temperature=0.1)

    llm_with_tools = llm.bind_tools(tools)

    def assistant(state: MessagesState):
        """Assistant Node"""
        messages = [sys_message] + state["messages"]
        result = llm_with_tools.invoke(messages)
        return {"messages": [result]}

    builder = StateGraph(MessagesState)
    builder.add_node("assistant", assistant)
    builder.add_node("tools", ToolNode(tools))
    builder.add_edge(START, "assistant")
    builder.add_edge("tools", "assistant")
    builder.add_conditional_edges(
        "assistant",
        tools_condition,
    )
    chat_graph = builder.compile()
    return chat_graph


if __name__ == '__main__':
    graph = build_graph("groq")
    question = """"What is the result of 3 + 2? just give me the final answer, do not give answers like:
    "The result is...", "The answer is...", "According to my analysis..."
    """
    messages = [HumanMessage(content=question)]
    messages = graph.invoke({"messages": messages})
    for m in messages["messages"]:
        m.pretty_print()
