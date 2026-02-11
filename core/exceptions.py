class ValidationError(Exception):
    """Raised when request validation fails."""
    pass


class AgentExecutionError(Exception):
    """Raised when agent execution fails."""
    pass
