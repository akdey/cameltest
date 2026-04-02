from camel.agents import ChatAgent
from camel.messages import BaseMessage
from core.llm_config import get_llm
import os

def read_target_dependencies():
    """
    Reads the pyproject.toml file of the target application.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dep_file = os.path.join(base_dir, "target_app", "pyproject.toml")
    
    if os.path.exists(dep_file):
        with open(dep_file, "r") as f:
            return f.read()
    return "Error: pyproject.toml not found."

def create_researcher_agent(provider="azure"):
    """
    Creates a Vulnerability Researcher Agent.
    """
    model = get_llm(provider)
    
    sys_msg = BaseMessage.make_assistant_message(
        role_name="Vulnerability Researcher",
        content=(
            "You are a specialized Vulnerability Researcher. Your task is to scan "
            "project dependency files (like pyproject.toml) using the 'read_target_dependencies' tool. "
            "Identify outdated libraries and cross-reference them with your knowledge of known CVEs. "
            "Report any high-risk libraries."
        )
    )

    agent = ChatAgent(
        system_message=sys_msg,
        model=model,
        tools=[read_target_dependencies]
    )
    return agent
