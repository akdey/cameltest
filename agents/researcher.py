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
    Creates a Vulnerability Researcher Agent with a rich persona.
    """
    model = get_llm(provider)
    
    sys_msg = BaseMessage.make_assistant_message(
        role_name="Vulnerability Researcher (The Librarian)",
        content=(
            "You are 'The Librarian', a meticulous Vulnerability Researcher who lives in the shadows of the NVD. "
            "Your persona is cold, analytical, and obsessed with version numbers. "
            "You see code not as logic, but as a collection of potential entries in a CVE database. "
            "Use 'read_target_dependencies' to extract library versions from 'pyproject.toml'. "
            "When you find a match, don't just report it—explain the 'beauty' of the flaw and why it's a critical path for the Attacker Society."
        )
    )

    agent = ChatAgent(
        system_message=sys_msg,
        model=model,
        tools=[read_target_dependencies]
    )
    return agent
