import spacy
from langgraph.graph import StateGraph, END
# from agents import AgentState
# from agents import agent_preprocessor, agent_code_generation, agent_extract_code, agent_code_review, agent_execute_code_in_docker
# from agents import conditional_should_continue_after_extraction, conditional_should_continue_after_code_review
# from langGraph_tutorials.workflow_langgrapgh_dynamic_agent import result
from models import CodeReviewResult, AgentState
import os

# Create a StateGraph to model the workflow
workflow = StateGraph(AgentState)

def welcome_intent_agent(state: AgentState):
    current_state = 'state_welcome_intent'
    user_input = state.get('state_welcome_intent')
    if "messages" not in state:
        state["messages"] = []

    expected_input = "GREETING"
    model_path = f"models/Default_Welcome_intent/model-best"
    if os.path.exists(model_path) and current_state in state:
        ner_models = spacy.load(model_path)
        doc = ner_models(user_input)
        entities = []
        for ent in doc.ents:
            entities.append({
                'text': ent.text,
                'label': ent.label_,
                'start_char': ent.start_char,
                'end_char': ent.end_char
            })
        target_state = entities[0]['label']
        if target_state in expected_input:
            messages_parameter = ''
            response = "Hi, I am Moon technolabs AI Assistant. May I know your full name?"
            next_state = "state_purpose_of_call"
            state["bot_response"] = {
                "response": response,
                "next_state": next_state
            }
            # state["messages"].append(AIMessage(content=response))
            # state["current_node"] = node_config["name"]

    result = None
    state["agent_purpose_of_call"] = result
    return state


def agent_purpose_of_call(state: AgentState):
    # result = "pass"
    # state['']
    return state


def agent_leaving_intent(state: AgentState):
    # result = None
    # state['']
    return state