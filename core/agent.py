"""
Agent module for HR Assistant AI.
Initializes and configures the LangGraph ReAct agent with tools and LLM.
"""
import os
import sys
from typing import Optional, List, Dict, Any

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage

from core.config import DEFAULT_LLM_MODEL, LLM_TEMPERATURE
from core.prompts import SYSTEM_PROMPT
from tools.sql_tools import get_hr_schema, execute_hr_sql
from tools.rag_tools import search_company_policies


def create_hr_agent(
    api_key: str,
    model_name: str = DEFAULT_LLM_MODEL,
    temperature: float = LLM_TEMPERATURE
):
    """
    Create a LangGraph ReAct agent equipped with SQL and RAG tools.

    Args:
        api_key: Google Gemini API key.
        model_name: Gemini model name (e.g. 'gemini-2.5-flash', 'gemini-2.5-pro').
        temperature: Sampling temperature for LLM.

    Returns:
        Compiled LangGraph ReAct agent.
    """
    llm = ChatGoogleGenerativeAI(
        model=model_name,
        google_api_key=api_key,
        temperature=temperature
    )

    tools = [
        get_hr_schema,
        execute_hr_sql,
        search_company_policies,
    ]

    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=SYSTEM_PROMPT
    )

    return agent


def format_chat_history(messages: List[Dict[str, str]]) -> List[BaseMessage]:
    """
    Convert Streamlit message history dictionaries into LangChain BaseMessage instances.

    Args:
        messages: List of dicts with keys 'role' ('user' or 'assistant') and 'content'.

    Returns:
        List of HumanMessage and AIMessage instances.
    """
    formatted = []
    for msg in messages:
        role = msg.get("role")
        content = msg.get("content", "")
        if role == "user":
            formatted.append(HumanMessage(content=content))
        elif role == "assistant":
            formatted.append(AIMessage(content=content))
    return formatted
