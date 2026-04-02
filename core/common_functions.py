import os

def get_env_var(name, default=None):
    """Retrieves an environment variable or returns a default value."""
    return os.environ.get(name, default)

def log_event(message, level="INFO"):
    """Simple logging utility for the simulation."""
    print(f"[{level}] {message}")
