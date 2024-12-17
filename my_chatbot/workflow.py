from langgraph.graph import StateGraph, END
from agents import AgentState
# from agents import agent_preprocessor, agent_code_generation, agent_extract_code, agent_code_review, agent_execute_code_in_docker
from agents import welcome_intent_agent, agent_purpose_of_call, agent_leaving_intent
# from agents import conditional_should_continue_after_extraction, conditional_should_continue_after_code_review


# Create a StateGraph to model the workflow
workflow = StateGraph(AgentState)

# Add nodes for each step
workflow.add_node("welcome_intent", welcome_intent_agent)
workflow.add_node("purpose_of_call", agent_purpose_of_call)
workflow.add_node("leaving_intent", agent_leaving_intent)
# workflow.add_node("agent_code_review", agent_code_review)
# workflow.add_node("agent_execute_code_in_docker", agent_execute_code_in_docker)

# Set entry point
workflow.set_entry_point("welcome_intent")

# Add edges between nodes
workflow.add_edge("welcome_intent", "purpose_of_call")
workflow.add_edge("purpose_of_call", "leaving_intent")

# # Add conditional edges
# workflow.add_conditional_edges(
#     "agent_extract_code",
#     conditional_should_continue_after_extraction,
#     {
#         "continue": "agent_code_review",
#         "regenerate": "agent_code_generation"
#     }
# )
#
# workflow.add_conditional_edges(
#     "agent_code_review",
#     conditional_should_continue_after_code_review,
#     {
#         "continue": "agent_execute_code_in_docker",
#         "regenerate": "agent_code_generation"
#     }
# )

workflow.add_edge("leaving_intent", END)

# Compile and run the workflow with debug messages
app = workflow.compile()

#helper method to visualize graph
def save_graph_to_file(runnable_graph, output_file_path):
    png_bytes = runnable_graph.get_graph().draw_mermaid_png()
    with open(output_file_path, 'wb') as file:
        file.write(png_bytes)

save_graph_to_file(app, "output.png")


def chat(initial_state):
    """Start an interactive chat session."""
    state = initial_state or {
        "state_initial_request": "Hello",
        "messages": [],
        "bot_response": "",
        "current_node": ""
    }
    print("Bot: Starting conversation...")
    while True:
        # Process current state
        result = app.invoke(state)

        print(f"Bot: {result['bot_response']}")

        if result.get("current_node") == "END":
            break

        if result.get("bot_response"):
            # next_state = ''
            # for next_node_state in self.config['workflow']['nodes']:
            #     seaching_key = next_node_state['logic']
            #     for next_node_value in seaching_key['response']:
            #         my_value = seaching_key['response'][next_node_value]
            #         if my_value == result.get("bot_response"):
            #             next_state_value = seaching_key['response_state'][next_node_value]
            #             next_state = next_state_value
            break

    return result.get("bot_response")



# Example usage
if __name__ == "__main__":
    # Initialize chatbot with configuration
    # chatbot = DynamicChatbot("27_nov.json")

    initial_state = {
        "state_welcome_intent": "Hello",
        # "state_purpose_of_call": "please cancel my room booking",
        # "state_room_cancellation": "i want to book my room",
        # "state_room_booking": "i want to book a room in indore",
        # "state_room_booking_id": "my booking id is 12345",
        "messages": [],
        "bot_response": "",
        "current_node": ""
    }

    result_final = chat(initial_state)