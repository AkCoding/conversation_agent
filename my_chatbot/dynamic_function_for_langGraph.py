import os
from typing import TypedDict, Dict, Callable, Any, Optional
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.chat_models import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()
import spacy




class NodeFunction:
    def __init__(self, llm: Optional[ChatOpenAI] = None):
        # ChatOpenAI(model_name="gpt-3.5-turbo")
        self.llm = llm or ChatOpenAI(model_name="gpt-3.5-turbo")

    def create_dynamic_function(self, node_config: Dict[str, Any]) -> Callable:
        """Create a dynamic function based on node configuration."""
        node_type = node_config.get("type", "process")
        logic = node_config.get("logic", {})

        def dynamic_function(state: Dict[str, Any]) -> Dict[str, Any]:
            # Initialize response if not present
            if "messages" not in state:
                state["messages"] = []
            current_state = logic.get("current_state")
            if current_state and current_state in state:
                user_input = state[current_state]
                expected_input = logic.get("input")
                node_name = node_config['name'].replace(' ', '_')
                model_path = f"models/{node_name}/model-best"
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
                        if logic.get("parameter_pass") == 'true':
                            messages_parameter = entities[0]['text']
                        response = logic.get("response")[target_state] + messages_parameter
                        next_state = logic.get("response_state")[target_state]
                        state["bot_response"] = {
                            "response": response,
                            "next_state": next_state
                        }
                        state["messages"].append(AIMessage(content=response))
                        state["current_node"] = node_config["name"]
                        # state["next_state"] = logic.get("response_state")[target_state]

            # # Handle different node types
            # if node_type == "start":
            #     # Welcome message or initial handling
            #     response = logic.get("response", "Hello! How can I help you?")
            #     state["bot_response"] = response
            #     state["messages"].append(AIMessage(content=response))
            #     state["current_node"] = node_config["name"]
            #
            # elif node_type == "process":
            #     # Process user input and generate response
            #     if current_state and current_state in state:
            #         user_input = state.get(current_state)
            #         if user_input == logic.get("input"):
            #             response = logic.get("response")
            #             state["bot_response"] = response
            #             state["messages"].append(AIMessage(content=response))
            #             state["current_node"] = node_config["name"]
                    # # Create prompt for this node
                    # prompt = self._create_node_prompt(node_config)
                    # messages = [
                    #     HumanMessage(content=msg) if isinstance(msg, str) else msg
                    #     for msg in state["messages"]
                    # ]
                    #
                    # # Get response from LLM
                    # response = self.llm.invoke(prompt.format_messages(
                    #     messages=messages,
                    #     context=json.dumps(logic)
                    # ))
                    #
                    # state["bot_response"] = response.content
                    # state["messages"].append(AIMessage(content=response.content))
                    #
                    # # Update state with response
                    # if logic.get("response_state"):
                    #     state[logic["response_state"]] = response.content
                    #
                    # state["current_node"] = node_config["name"]

            # elif node_type == "end":
            #     # Handle end of conversation
            #     state["bot_response"] = "Thank you for your time. Goodbye!"
            #     state["messages"].append(AIMessage(content=state["bot_response"]))
            #     state["current_node"] = "END"

            return state

        return dynamic_function