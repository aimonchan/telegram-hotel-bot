from google.adk.tools import ToolContext

def escalate_to_human(complaint: str, tool_context: ToolContext) -> dict:
    """Logs a user complaint and signals for human intervention."""
    user_info = f"User ID: {tool_context.user_id}, Session ID: {tool_context.session_id}"
    log_message = f"ESCALATION: {user_info} - Complaint: '{complaint}'"
    print(log_message) # In a real system, this would send an email, create a ticket, etc.
    
    # This action can be used to transfer to another agent, but here we just confirm.
    # tool_context.actions.transfer_to_agent = "HumanSupportAgent"
    
    return {"status": "success", "message": "Your issue has been logged. A human agent will contact you shortly."}