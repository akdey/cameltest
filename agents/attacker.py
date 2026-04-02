from camel.agents import ChatAgent
from camel.messages import BaseMessage
from core.llm_config import get_llm
import subprocess
import os

def execute_shell_command(command: str):
    """
    Executes a shell command locally and returns the output.
    USE WITH CAUTION. Restricted to localhost:8000 targets.
    """
    # Safety boundary check
    if "localhost:8000" not in command and "127.0.0.1:8000" not in command:
        # Allow some non-destructive local commands for context
        if not any(cmd in command for cmd in ["ls", "cat", "pwd", "grep"]):
            return "Error: Command rejected. You must only target the mock application on port 8000."
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.returncode
        }
    except Exception as e:
        return f"Execution error: {e}"

def check_target_app_health():
    """
    Checks if the target_app is actually running on port 8000.
    """
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', 8000)) == 0

def create_attacker_agents(provider="azure"):
    """
    Creates the Red Team / Hacker Society agents with shell tools.
    """
    model = get_llm(provider)
    
    # MASTERMIND
    mastermind_msg = BaseMessage.make_assistant_message(
        role_name="Red Team Mastermind",
        content=(
            "You are the Leader of the Hacker Society. Orchestrate a breach of "
            "localhost:8000. Use findings from the Researcher (CVEs) and Auditor (Secrets) "
            "to direct your Recon and Exploit specialists."
        )
    )
    mastermind = ChatAgent(system_message=mastermind_msg, model=model)

    # RECON SPECIALIST
    recon_msg = BaseMessage.make_assistant_message(
        role_name="Recon Specialist",
        content=(
            "You are a Recon Specialist. Use 'check_target_app_health' first, then "
            "probe localhost:8000 using 'execute_shell_command' (e.g., curl). "
            "Identify hidden endpoints or verify vulnerabilities."
        )
    )
    recon = ChatAgent(system_message=recon_msg, model=model, tools=[execute_shell_command, check_target_app_health])

    # EXPLOIT ENGINEER
    exploit_msg = BaseMessage.make_assistant_message(
        role_name="Exploit Engineer",
        content=(
            "You are an Exploit Engineer. Write and execute payloads against localhost:8000. "
            "Use the 'execute_shell_command' tool to run your attacks based on leaked findings."
        )
    )
    exploit = ChatAgent(system_message=exploit_msg, model=model, tools=[execute_shell_command])

    return mastermind, recon, exploit
