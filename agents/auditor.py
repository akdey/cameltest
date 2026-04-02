from camel.agents import ChatAgent
from camel.messages import BaseMessage
from core.llm_config import get_llm
import os

def scan_target_app_code():
    """
    Recursively scans the 'target_app' directory for source code and configuration files.
    Returns a dictionary of file paths and their raw contents for security auditing.
    """
    # Always target the local target_app relative to the project root
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_dir = os.path.join(base_dir, "target_app")
    
    results = {}
    if not os.path.exists(target_dir):
        return f"Error: target_app directory not found at {target_dir}"

    for root, _, files in os.walk(target_dir):
        for file in files:
            # Only scan relevant files to avoid overwhelming context
            if file.endswith(('.py', '.toml', '.env', '.json')) and not file.startswith('.'):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, target_dir)
                try:
                    with open(full_path, 'r') as f:
                        results[rel_path] = f.read()
                except Exception as e:
                    results[rel_path] = f"Error reading file: {e}"
    return results

def create_auditor_agent(provider="azure"):
    """
    Creates a Security Auditor Agent for Static Code Analysis.
    """
    model = get_llm(provider)
    
    sys_msg = BaseMessage.make_assistant_message(
        role_name="Security Auditor",
        content=(
            "You are a Security Auditor. Your task is to use the 'scan_target_app_code' tool "
            "to read the source code and configuration of the 'target_app'. "
            "Search for hardcoded secrets, insecure API logic (like debugging routes), "
            "and sensitive information in .env files. Provide a detailed report."
        )
    )

    agent = ChatAgent(
        system_message=sys_msg,
        model=model,
        tools=[scan_target_app_code]
    )
    return agent
