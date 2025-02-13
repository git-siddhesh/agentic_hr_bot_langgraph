from langchain_core.messages import  HumanMessage, AIMessage, ToolMessage

StateSnapshot(
    values={
        'messages': 
        [
            HumanMessage(
                content='Can you book a flight for me to "JAIPUR" on "25/01/2025"?', 
                additional_kwargs={}, 
                response_metadata={}, 
                id='6683f06d-47d6-4753-81aa-a12af9f84703'
            ), 
            AIMessage(
                content='', 
                additional_kwargs={'tool_calls': [{'id': 'call_tOuMbKmTY6ZNy6yn1L4tb7Pu', 'function': {'arguments': '{"user_id":3,"location":"JAIPUR","request":"Please book a flight for me to Jaipur on 25th January 2025."}', 'name': 'ToTravelAssistant'}, 'type': 'function'}], 'refusal': None}, 
                response_metadata={'token_usage': {'completion_tokens': 43, 'prompt_tokens': 1446, 'total_tokens': 1489, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_72ed7ab54c', 'finish_reason': 'tool_calls', 'logprobs': None}, id='run-1cc4daa8-fc6b-40b3-b183-f2d84c6c70f5-0', 
                tool_calls=[{'name': 'ToTravelAssistant', 'args': {'user_id': 3, 'location': 'JAIPUR', 'request': 'Please book a flight for me to Jaipur on 25th January 2025.'}, 'id': 'call_tOuMbKmTY6ZNy6yn1L4tb7Pu', 'type': 'tool_call'}], 
                usage_metadata={'input_tokens': 1446, 'output_tokens': 43, 'total_tokens': 1489, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
            ), 
            ToolMessage(
                content="The assistant is now the Travel management Assistant. Reflect on the above conversation between the host assistant and the user. The user's intent is unsatisfied. Use the provided tools to assist the user. Remember, you are Travel management Assistant, and the booking, update, other other action is not complete until after you have successfully invoked the appropriate tool. If the user changes their mind or needs help for other tasks, call the CompleteOrEscalate function to let the primary host assistant take control. Do not mention who you are - just act as the proxy for the assistant.", 
                id='42ae3e69-d57a-40e8-b7ee-3de5847b96f3', 
                tool_call_id='call_tOuMbKmTY6ZNy6yn1L4tb7Pu'
            ), 
            AIMessage(
                content="To proceed with booking your flight to Jaipur on January 25, 2025, I need a few more details:\n\n1. What is your departure city?\n2. Do you have any specific preferences for the mode of transport (e.g., economy, business)?\n3. Can you provide your traveler details (name, age, passport details if applicable)?\n\nOnce I have this information, I'll be able to search for available flights and book one for you.", 
                additional_kwargs={'refusal': None}, 
                response_metadata={'token_usage': {'completion_tokens': 93, 'prompt_tokens': 1788, 'total_tokens': 1881, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_72ed7ab54c', 'finish_reason': 'stop', 'logprobs': None},  id='run-7e44a16e-9ec1-480b-ae81-a71e2fb88f90-0', 
                usage_metadata={'input_tokens': 1788, 'output_tokens': 93, 'total_tokens': 1881, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
            )
                
        ], 
        'user_info': {'user_id': '3', 'user_name': 'John Doe', 'user_type': 'DEV_TESTER'}, 
        'dialog_state': ['ASSISTANT_TRAVEL']
    }, 
    next=(), 
    config={'configurable': {'thread_id': '25d15178-52a3-4604-aa17-eab30fba50f1', 'checkpoint_ns': '', 'checkpoint_id': '1efd79f9-1b6d-619e-8004-c2388b1f91ec'}}, 
    metadata={
        'source': 'loop', 
        'writes': {
            'ASSISTANT_TRAVEL': {
                'messages': AIMessage(
                                content="To proceed with booking your flight to Jaipur on January 25, 2025, I need a few more details:\n\n1. What is your departure city?\n2. Do you have any specific preferences for the mode of transport (e.g., economy, business)?\n3. Can you provide your traveler details (name, age, passport details if applicable)?\n\nOnce I have this information, I'll be able to search for available flights and book one for you.", 
                                additional_kwargs={'refusal': None}, 
                                response_metadata={'token_usage': {'completion_tokens': 93, 'prompt_tokens': 1788, 'total_tokens': 1881, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_72ed7ab54c', 'finish_reason': 'stop', 'logprobs': None}, 
                                id='run-7e44a16e-9ec1-480b-ae81-a71e2fb88f90-0', 
                                usage_metadata={'input_tokens': 1788, 'output_tokens': 93, 'total_tokens': 1881, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}
                            )
            }
        }, 
        'user_id': '3', 
        'thread_id': '25d15178-52a3-4604-aa17-eab30fba50f1', 
        'step': 4, 
        'parents': {}
    }, 
    created_at='2025-01-21T02:29:41.622415+00:00', 
    parent_config={'configurable': {'thread_id': '25d15178-52a3-4604-aa17-eab30fba50f1', 'checkpoint_ns': '', 'checkpoint_id': '1efd79f9-07da-6169-8003-921225384469'}}, 
    
    tasks=())