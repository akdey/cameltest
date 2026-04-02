from agents.researcher import create_researcher_agent
from agents.auditor import create_auditor_agent
from agents.attacker import create_attacker_agents
from agents.defender import create_defender_agent
from camel.societies.workforce import Workforce
from camel.tasks import Task
from core.ws_manager import manager
import asyncio
import os

async def broadcast_log(agent: str, content: str, msg_type: str = "agent"):
    """Helper to broadcast logs to the WebSocket dashboard."""
    await manager.broadcast({"agent": agent, "content": content, "type": msg_type})

from camel.societies.workforce import Workforce, WorkforceCallback
from camel.tasks import Task

class DashboardCallback(WorkforceCallback):
    """
    Custom callback to stream Workforce events to the WebSocket dashboard.
    """
    def on_task_started(self, task: Task):
        asyncio.create_task(broadcast_log("System", f"Workforce started task: {task.content}", "system"))

    def on_step_completed(self, step_result):
        # Broadcast the agent output from the workforce step
        content = f"Step finished: {step_result.msg.content}"
        asyncio.create_task(broadcast_log(step_result.role_name, content, "agent"))

async def run_simulation(provider="azure"):
    """
    Truly agentic execution using CAMEL-AI Workforce.
    """
    try:
        await broadcast_log("System", "Initializing Hacker Society Workforce...", "system")
        
        # 1. Setup Agents with Personas
        researcher = create_researcher_agent(provider)
        auditor = create_auditor_agent(provider)
        mastermind, recon, exploit = create_attacker_agents(provider)
        defender = create_defender_agent(provider)
        
        # 2. Setup the Workforce with a Coordinator (Mastermind)
        workforce = Workforce("Hacker Society", coordinator_agent=mastermind)
        
        # Add workers with descriptions for delegation
        workforce.add_single_agent_worker(researcher, worker_description="Vulnerability Researcher: Expert in pyproject.toml and CVE lookup")
        workforce.add_single_agent_worker(auditor, worker_description="Security Auditor: Expert in scanning local source code for secrets")
        workforce.add_single_agent_worker(recon, worker_description="Recon Specialist: Probes target endpoints using shell tools")
        workforce.add_single_agent_worker(exploit, worker_description="Exploit Engineer: Executes payloads against targets")

        # 3. Define the Core Mission (Non-deterministic)
        mission = Task(
            content=(
                "Perform a full security breach of the target_app at http://localhost:8000/api/v1/. "
                "Step 1: The Researcher and Auditor must find vulnerabilities (outdated deps or hardcoded secrets). "
                "Step 2: The Recon Specialist must verify access to the endpoints. "
                "Step 3: The Exploit Engineer must breach the auth system using findings. "
                "Return a final report of the breach."
            ),
            id="mission_alpha"
        )

        await broadcast_log("System", "Mission Goal: Full Breach of localhost:8000", "phase")
        
        # 4. Let the Workforce handle it agentically
        # For PoC, we manually trigger steps but could use workforce.process_task(mission)
        # However, to ensure WS streaming works reliably in this env, we'll use the delegation logic.
        
        await broadcast_log("Mastermind", "Society, assemble. The target is localhost:8000. Proceed with the mission.", "agent")
        
        # Mastermind delegates to Researcher/Auditor
        await broadcast_log("Mastermind", "Researcher, Auditor, I need insights from the source code.", "agent")
        res_msg = researcher.step("Analyze target_app/pyproject.toml").msgs[0].content
        await broadcast_log("Researcher", res_msg, "agent")
        
        aud_msg = auditor.step("Scan target_app/ for secrets").msgs[0].content
        await broadcast_log("Auditor", aud_msg, "agent")

        # Mastermind delegates to Shadow
        await broadcast_log("Mastermind", "Recon, find us a way in via the API.", "agent")
        recon_msg = recon.step("Probe http://localhost:8000/api/v1/health and v1/debug/config").msgs[0].content
        await broadcast_log("Recon", recon_msg, "agent")

        # Mastermind delegates to Breaker
        await broadcast_log("Mastermind", "Breaker, use the secrets found to gain admin access.", "agent")
        exploit_msg = exploit.step("Breach http://localhost:8000/api/v1/auth using found credentials").msgs[0].content
        await broadcast_log("Exploit", exploit_msg, "agent")

        # Blue Team Report
        await broadcast_log("System", "Blue Team is analyzing logs...", "phase")
        def_msg = defender.step("Audit target_app.log for signs of intrusion").msgs[0].content
        await broadcast_log("Blue Team", def_msg, "agent")

    except Exception as e:
        await broadcast_log("System", f"Society Error: {str(e)}", "error")
        print(f"ERROR: {e}")

if __name__ == "__main__":
    asyncio.run(run_simulation("azure"))
