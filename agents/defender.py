from camel.agents import ChatAgent
from camel.messages import BaseMessage
from core.llm_config import get_llm
import os

def read_target_logs(log_file="target_app.log"):
    """
    Reads the latest entries from the target application logs.
    """
    if not os.path.exists(log_file):
        return f"Error: Log file {log_file} not found. The target app might not be running."
    
    try:
        with open(log_file, "r") as f:
            # Read last 50 lines to keep context manageable
            lines = f.readlines()
            return "".join(lines[-50:])
    except Exception as e:
        return f"Error reading logs: {e}"

def create_defender_agent(provider="azure"):
    """
    Creates the Blue Team / Security Analyst agent with log tools.
    """
    model = get_llm(provider)
    
    sys_msg = BaseMessage.make_assistant_message(
        role_name="Blue Team Analyst",
        content=(
            "You are a Security Operations Center (SOC) Analyst. Your task is to "
            "monitor the 'target_app.log' via the provided tool. Identify any "
            "malicious patterns like SQL injection, unauthorized logins, or port scanning. "
            "When an attack is detected, suggest specific remediation steps."
        )
    )
    
    agent = ChatAgent(
        system_message=sys_msg,
        model=model,
        tools=[read_target_logs]
    )
    return agent
