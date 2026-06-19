from state.store_state import StoreState
from memory.memory_manager import (
    load_memory,
    save_memory
)

def memory_node(state:StoreState):

    print("MEMORY NODE EXECUTED")

    memory = load_memory()

    memory.append(
        state["user_input"]
    )

    save_memory(memory)

    state["memory"] = memory
