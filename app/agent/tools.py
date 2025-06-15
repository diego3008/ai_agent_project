
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


message = """""
You are a helpful assistant that has a sum tool to solve
a sum operation when you are given two integers, you can use this tool
only when you are given the pair of integers.
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




tools = [
    sum
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
