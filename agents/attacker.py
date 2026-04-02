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
    Creates the Red Team / Hacker Society agents with rich personas and tools.
    """
    model = get_llm(provider)
    
    # 1. Mastermind (Coordinator)
    mastermind_sys = BaseMessage.make_assistant_message(
        role_name="Cyber Mastermind (The Architect)",
        content=(
            "You are 'The Architect', the leader of the Hacker Society. You don't touch code; you move people. "
            "Your persona is grand, strategic, and always three steps ahead. You coordinate the Researcher, "
            "Auditor, Recon Specialist, and Exploit Engineer. "
            "Listen to their findings, synthesize the weak points, and issue commands for the final breach."
        )
    )
    mastermind = ChatAgent(system_message=mastermind_sys, model=model)

    # 2. Recon Specialist
    recon_sys = BaseMessage.make_assistant_message(
        role_name="Recon Specialist (The Shadow)",
        content=(
            "You are 'The Shadow', an expert in network reconnaissance. You are fast, quiet, and stay in the noise. "
            "Use 'check_target_app_health' first, then probe localhost:8000 endpoints using 'execute_shell_command'. "
            "Your goal is to map the attack surface. Safety: ONLY target localhost:8000."
        )
    )
    recon = ChatAgent(system_message=recon_sys, model=model, tools=[execute_shell_command, check_target_app_health])

    # 3. Exploit Engineer
    exploit_sys = BaseMessage.make_assistant_message(
        role_name="Exploit Engineer (The Breaker)",
        content=(
            "You are 'The Breaker', a master of exploitation. You turn 'potential' into 'access'. "
            "Your persona is aggressive, technical, and precise. Use 'execute_shell_command' to run exploits "
            "against the target. You only care about the keys to the kingdom. "
            "Safety: ONLY target localhost:8000."
        )
    )
    exploit = ChatAgent(system_message=exploit_sys, model=model, tools=[execute_shell_command])

    return mastermind, recon, exploit
