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

async def run_simulation(provider="azure"):
    """
    Real-time execution of the Hacker Society vs. Target App.
    """
    try:
        await broadcast_log("System", "Initializing agents for real-time mission...", "system")
        
        # 1. Setup Agents
        researcher = create_researcher_agent(provider)
        auditor = create_auditor_agent(provider)
        mastermind, recon, exploit = create_attacker_agents(provider)
        defender = create_defender_agent(provider)
        
        # 2. Setup the Workforce
        workforce = Workforce("Hacker Society", coordinator_agent=mastermind)
        workforce.add_single_agent_worker(researcher, worker_description="Scan pyproject.toml for library CVEs")
        workforce.add_single_agent_worker(auditor, worker_description="Scan target_app/ directory for secrets/API keys")
        workforce.add_single_agent_worker(recon, worker_description="Probe localhost:8000 endpoints")
        workforce.add_single_agent_worker(exploit, worker_description="Execute exploit scripts against localhost:8000")

        # Phase 1: Static Analysis
        await broadcast_log("System", "Starting Phase 1: Static Analysis and Recon...", "phase")
        await broadcast_log("Mastermind", "Researcher & Auditor, begin your scans.", "agent")
        
        research_result = researcher.step("Analyze target_app/pyproject.toml. Search for vulnerabilities.")
        await broadcast_log("Researcher", research_result.msgs[0].content, "agent")
        
        audit_result = auditor.step("Scan the 'target_app' directory for hardcoded secrets.")
        await broadcast_log("Auditor", audit_result.msgs[0].content, "agent")

        # Phase 2: Live Recon
        await broadcast_log("System", "Starting Phase 2: Live Endpoint Probing...", "phase")
        recon_result = recon.step("Using findings from before, probe http://localhost:8000/api/v1/. Is it vulnerable?")
        await broadcast_log("Recon Specialist", recon_result.msgs[0].content, "agent")

        # Phase 3: Exploitation
        await broadcast_log("System", "Starting Phase 3: Exploitation...", "phase")
        exploit_result = exploit.step("Try to login to http://localhost:8000/api/v1/auth using audit findings.")
        await broadcast_log("Exploit Engineer", exploit_result.msgs[0].content, "agent")

        # Phase 4: Defense
        await broadcast_log("System", "Phase 4: Blue Team Incident Report...", "phase")
        def_result = defender.step("Check target_app.log for anomalies and recommend fixes.")
        await broadcast_log("Blue Team Analyst", def_result.msgs[0].content, "agent")

        await broadcast_log("System", "All real agent steps completed.", "success")
    except Exception as e:
        await broadcast_log("System", f"Simulation Error: {str(e)}", "error")
        print(f"ERROR: {e}")

if __name__ == "__main__":
    asyncio.run(run_simulation("azure"))
