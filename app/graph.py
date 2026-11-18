"""
StartupSetu LangGraph Agent with Memory & Human Approval Step
Constructs a stateful agent graph powered by LangGraph, featuring:
- MemorySaver checkpointer for multi-turn conversational context
- Automatic routing between RAG and domain tools
- Explicit human approval step (HITL) before executing mutating actions (submit_dpiit_application)
"""

import uuid
from typing import Any, TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph

from app.agent_loop import _heuristic_decision, _parse_llm_action
from app.llm import generate_response
from app.tools import (
    AVAILABLE_TOOLS,
    check_dpiit_eligibility,
    get_scheme_details,
    query_rag,
    submit_dpiit_application,
)


class AgentState(TypedDict):
    query: str
    messages: list[dict[str, str]]
    thread_id: str
    action: str | None
    action_input: dict[str, Any]
    observation: Any | None
    answer: str
    citations: list[dict[str, Any]]
    requires_approval: bool
    approved: bool | None
    pending_action: dict[str, Any] | None
    status: str  # "completed" | "needs_approval"


# --------------------------------------------------
# GRAPH NODES
# --------------------------------------------------

def reason_node(state: AgentState) -> dict[str, Any]:
    """
    Analyzes the latest user message and determines the next action.
    If resuming with an approved/rejected pending action, routes accordingly.
    """
    query = state.get("query", "").strip()
    approved = state.get("approved")
    pending = state.get("pending_action")

    # If already awaiting approval and user responded
    if pending and approved is not None:
        if approved:
            return {
                "action": pending.get("tool"),
                "action_input": pending.get("parameters", {}),
                "requires_approval": False,
                "pending_action": None,
                "status": "in_progress"
            }
        else:
            return {
                "action": "cancel",
                "action_input": {},
                "requires_approval": False,
                "pending_action": None,
                "answer": f"Action '{pending.get('tool')}' was rejected by user.",
                "status": "completed"
            }

    # Reason on fresh query
    action = None
    action_input: dict[str, Any] = {}

    # Check via LLM if available
    try:
        llm_out = generate_response(
            f"Analyze founder query and pick tool or answer: {query}"
        )
        parsed = _parse_llm_action(llm_out)
        if parsed.get("action") in AVAILABLE_TOOLS:
            action = parsed["action"]
            action_input = parsed.get("action_input", {})
    except Exception:
        pass

    # Heuristic fallback
    if not action:
        heuristic = _heuristic_decision(query)
        action = heuristic["action"]
        action_input = heuristic["action_input"]

    # Check if this tool requires human approval
    SENSITIVE_TOOLS = ["submit_dpiit_application"]
    if action in SENSITIVE_TOOLS and not approved:
        return {
            "action": action,
            "action_input": action_input,
            "requires_approval": True,
            "pending_action": {
                "tool": action,
                "parameters": action_input
            },
            "status": "needs_approval"
        }

    return {
        "action": action,
        "action_input": action_input,
        "requires_approval": False,
        "pending_action": None,
        "status": "in_progress"
    }


def approval_node(state: AgentState) -> dict[str, Any]:
    """
    Human-in-the-loop checkpoint node.
    Pauses execution and requests explicit human confirmation.
    """
    pending = state.get("pending_action", {})
    tool_name = pending.get("tool", "Sensitive Action")
    params = pending.get("parameters", {})

    approval_message = (
        f"⚠️ **Approval Required Before Execution**\n\n"
        f"The agent is preparing to execute: `{tool_name}` with the following parameters:\n"
        f"```json\n{params}\n```\n\n"
        f"Do you approve this submission? Please respond with approval to proceed."
    )

    return {
        "answer": approval_message,
        "status": "needs_approval"
    }


def tool_node(state: AgentState) -> dict[str, Any]:
    """
    Executes the decided tool and stores observation.
    """
    action = state.get("action")
    action_input = state.get("action_input", {})
    citations = list(state.get("citations", []))

    if action == "cancel":
        return {
            "observation": {"status": "cancelled"},
            "status": "completed"
        }

    observation: Any = None
    if action == "query_rag":
        q = action_input.get("question", state.get("query", ""))
        observation = query_rag(question=q)
        if isinstance(observation, dict):
            citations.extend(observation.get("citations", []))

    elif action == "check_dpiit_eligibility":
        observation = check_dpiit_eligibility(
            entity_type=action_input.get("entity_type", "Private Limited Company"),
            incorporation_year=action_input.get("incorporation_year", 2024),
            annual_turnover_cr=action_input.get("annual_turnover_cr", 1.0),
            is_innovative=action_input.get("is_innovative", True)
        )
        citations.append({
            "title": "DPIIT Startup Recognition Guidelines",
            "page": 1,
            "source": "https://www.startupindia.gov.in/content/sih/en/startupgov/startup_recognition_page.html"
        })

    elif action == "get_scheme_details":
        scheme_q = action_input.get("scheme_query", state.get("query", ""))
        observation = get_scheme_details(scheme_query=scheme_q)
        scheme = observation.get("scheme", {})
        if scheme:
            citations.append({
                "title": scheme.get("name", "Government Scheme"),
                "page": 1,
                "source": scheme.get("portal", "https://www.startupindia.gov.in/")
            })

    elif action == "submit_dpiit_application":
        observation = submit_dpiit_application(
            startup_name=action_input.get("startup_name", "Student Venture"),
            entity_type=action_input.get("entity_type", "Private Limited Company"),
            founder_name=action_input.get("founder_name", "Founder"),
            email=action_input.get("email", "founder@example.com"),
            sector=action_input.get("sector", "Technology")
        )

    return {
        "observation": observation,
        "citations": citations,
        "status": "synthesizing"
    }


def synthesize_node(state: AgentState) -> dict[str, Any]:
    """
    Synthesizes the final user response from tool observation and query context.
    """
    action = state.get("action")
    obs = state.get("observation")
    existing_answer = state.get("answer")

    if existing_answer and action == "cancel":
        final_answer = existing_answer
    elif action == "query_rag" and isinstance(obs, dict):
        final_answer = obs.get("answer", "")
    elif action == "check_dpiit_eligibility" and isinstance(obs, dict):
        verdict = "ELIGIBLE" if obs.get("is_eligible") else "NOT ELIGIBLE"
        final_answer = (
            f"### DPIIT Startup Recognition Assessment: **{verdict}**\n\n"
            f"{obs.get('summary')}\n\n"
            f"- **Entity Type Valid:** {obs.get('criteria', {}).get('entity_type_valid')}\n"
            f"- **Age <= 10 Years:** {obs.get('criteria', {}).get('age_under_10_years')} ({obs.get('years_active')} yrs)\n"
            f"- **Turnover <= ₹100 Cr:** {obs.get('criteria', {}).get('turnover_under_100cr')} (₹{obs.get('annual_turnover_cr')} Cr)\n"
            f"- **Innovation/Scalability:** {obs.get('criteria', {}).get('innovative_scalable')}\n\n"
        )
        if obs.get("recommended_benefits"):
            final_answer += "#### Available Benefits:\n"
            for b in obs["recommended_benefits"]:
                final_answer += f"- {b}\n"
    elif action == "get_scheme_details" and isinstance(obs, dict):
        scheme = obs.get("scheme", {})
        if scheme:
            final_answer = (
                f"### {scheme.get('name')}\n\n"
                f"- **Funding:** {scheme.get('funding')}\n"
                f"- **Eligibility:** {scheme.get('eligibility')}\n"
                f"- **Category:** {scheme.get('category')}\n"
                f"- **Official Portal:** [{scheme.get('name')}]({scheme.get('portal')})\n"
            )
        else:
            final_answer = obs.get("message", "Scheme details unavailable.")
    elif action == "submit_dpiit_application" and isinstance(obs, dict):
        final_answer = (
            f"✅ **Application Approved & Submitted Successfully**\n\n"
            f"{obs.get('message')}\n\n"
            f"Official tracking ID and confirmation have been registered."
        )
    else:
        final_answer = "Your inquiry has been processed by StartupSetu Agent."

    # Update conversation history
    messages = list(state.get("messages", []))
    messages.append({"role": "user", "content": state.get("query", "")})
    messages.append({"role": "assistant", "content": final_answer})

    return {
        "answer": final_answer,
        "messages": messages,
        "status": "completed"
    }


def route_decision(state: AgentState) -> str:
    """Conditional router based on reason_node evaluation."""
    if state.get("status") == "needs_approval":
        return "approval_node"
    return "tool_node"


# --------------------------------------------------
# COMPILE GRAPH
# --------------------------------------------------

def build_agent_graph():
    builder = StateGraph(AgentState)

    builder.add_node("reason_node", reason_node)
    builder.add_node("approval_node", approval_node)
    builder.add_node("tool_node", tool_node)
    builder.add_node("synthesize_node", synthesize_node)

    builder.add_edge(START, "reason_node")
    builder.add_conditional_edges(
        "reason_node",
        route_decision,
        {
            "approval_node": "approval_node",
            "tool_node": "tool_node"
        }
    )
    builder.add_edge("approval_node", END)
    builder.add_edge("tool_node", "synthesize_node")
    builder.add_edge("synthesize_node", END)

    memory = MemorySaver()
    return builder.compile(checkpointer=memory)


agent_graph = build_agent_graph()


def run_graph_agent(
    query: str,
    thread_id: str | None = None,
    approved: bool | None = None
) -> dict[str, Any]:
    """
    Run the LangGraph agent with session memory and human approval support.
    """
    active_thread_id = thread_id or f"session-{uuid.uuid4().hex[:8]}"
    config = {"configurable": {"thread_id": active_thread_id}}

    current_state = agent_graph.get_state(config)
    if current_state and current_state.values:
        input_data = {"query": query}
        if approved is not None:
            input_data["approved"] = approved
        final_state = agent_graph.invoke(input_data, config=config)
    else:
        initial_state: AgentState = {
            "query": query,
            "messages": [],
            "thread_id": active_thread_id,
            "action": None,
            "action_input": {},
            "observation": None,
            "answer": "",
            "citations": [],
            "requires_approval": False,
            "approved": approved,
            "pending_action": None,
            "status": "started"
        }
        final_state = agent_graph.invoke(initial_state, config=config)

    return {
        "response": final_state.get("answer", ""),
        "thread_id": active_thread_id,
        "status": final_state.get("status", "completed"),
        "citations": final_state.get("citations", []),
        "requires_approval": final_state.get("requires_approval", False),
        "pending_action": final_state.get("pending_action")
    }


if __name__ == "__main__":
    print("Testing LangGraph Agent with memory and approval step...")
    res1 = run_graph_agent("What is DPIIT Startup Recognition?")
    print("Direct RAG query status:", res1["status"])
    print("Response:\n", res1["response"][:200])

    print("\nTesting Approval Trigger...")
    res2 = run_graph_agent("Please submit my application for startup registration")
    print("Approval status:", res2["status"])
    print("Pending action:", res2["pending_action"])

    print("\nTesting Approval Confirmation with thread_id...")
    res3 = run_graph_agent(
        "Confirming submission",
        thread_id=res2["thread_id"],
        approved=True
    )
    print("After approval status:", res3["status"])
    print("Response:\n", res3["response"])
