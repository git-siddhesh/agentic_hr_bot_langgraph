# Title: Digital farming agentic bot: 

# Following are the agents and the tools associated with a DIGITAL_FARMING agentic bot
from tools.rag import lookup_policy
from tools.chat_session import sessoion_details
from tools.rag import lookup_policy
from tools.runnable.user_profile import search_directory, view_directory_stats, verify_profile, view_profile, update_profile, send_message, initiate_registration, deactivate_profile, generate_contact_list, add_emergency_contact



# Expected Output:
List of Agents with description 
for each agent a set of tools that can be executed

# Current Plan/Flow for Digital Green

## Description: 
We need to create a agentic solution for the farmers in india. 
this bot can be run on whatsapp or any other multimedia chat platform
## Code idea: proposed by openai to govt of idea
Extension agents teach farmers best practices for growing their crops, help them connect with local suppliers, and provide market and pricing information. But especially in rural, remote communities, giving every farmer the support they need is a huge challenge. 
It provides language specific translation (input and output)
Work as a self-teaching tool to grow their own expertise. 

# Example use case:

USER: There seems to be issue with my crop, can you help me with the issue?
My location: 22.5726° N, 88.3639° E

BOT: Yes sure I will help you with that. Please provide me with the following information:
- Description of the issue
- Crop name/Type
- Image of the crop

USER: there are some brwon insects on my crop. + [Image of the crop]

BOT: The image is not clear, can you please provide me with a clear image of the crop?

USER: [Clear image of the crop]

BOT: I have identified the issue, it seems to be a case of pest infestation. I will provide you with the solution for the same.
You can use the following pesticide to get rid of the pest.
- [Pesticide name]
Counter question: Do you have any allergies to the pesticide?

...

# Must have agents or tools
- Translation tool
- Multi-modal conversion too (speech to text tool and tts)
- Image processing agent: Will take the image in input and extract the key features out of it (will use openAI o1). Given the query and use-intent it will create the instructions/commands for the image model to extract or detect specific information out of the image (o1 model has general extraction so we need specific input for the model to generate output)
