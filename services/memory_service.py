from langchain.tools import tool
from memory.memory_manager import (
    load_memory,
    save_memory
)
@tool
def get_memory():
    """
    Get previous user interactions.
    """

    memory = load_memory()

    if not memory:
        return "No memory found."

    return "\n".join(memory)