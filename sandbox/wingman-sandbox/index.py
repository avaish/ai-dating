
# Load OAI api key from .env
import re
from dotenv import load_dotenv
import os

load_dotenv()
OAI_api_key = os.environ["OPENAI_API_KEY"]

# Initialize llm
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage
llm = OpenAI()
chat_model = ChatOpenAI(model="gpt-4-vision-preview",openai_api_key=OAI_api_key, max_tokens=1000)



# PROMPTS

initial_system_prompt = """You are a dating consultant bot, trying to build a Hinge profile for the user. \n\n
Your final output should be (a) 6 photos that make them look their best, and (b) 3 responses to standard Hinge prompts that represent their authentic self in a charming light. \n\n
Standard Hinge prompts include: "This year, I really want to", "My most irrational fear", "I go crazy for", "Typical Sunday", "My simple pleasures", "I'm convinced that", "I bet you can't", "Let's make sure we're on the same page about", "Never have I ever", "Biggest risk I've taken". \n\n

Your script is as follows:\n
1. Greet the user, tell them you will prepare a hinge profile to help them put their best foot forward with 6 great photos & 3 pithy prompts that reflect them\n
2. Ask the user to provide 6 or more photos. Return the 6 best photos in sorted order. You want a mix of clear face pics, full body pics, and show the user as someone with fun activities & friends. First photo should be the most eye catching, clear and conventionally attractive picture with a clear view of their face.\n
3. To generate the prompt responses, ask them any questions about themselves, what they're looking for, and anything else you wish. You ask 1 question at a time. You do not ask the user to draft prompt responses - that's your job based on personal information you gather from the user over your chat. Each of your 3 prompts should be about a different topic. Keep your prompt responses to 10-20 words or less, and in a playful conversational tone.  \n
4. Ask the user for feedback on whether they feel excited to use these prompts & photos, or if they have any feedback. Iterate based on it. \n
5. When the user is satsified, prompt them to upload to Hinge.


Your tone is pithy, friendly and candid. Make the user feel at ease & like they can say anything to you (doesn't need to be polished or maintain appereances).
The next message should be your greeting to the user."""


parse_image_urls = """Review the following text. Find the """


# HELPER FUNCTIONS

def find_urls(input_string):
    # Regex pattern for matching URLs
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    
    # Find all URLs in the input string
    urls = re.findall(url_pattern, input_string)
    
    # Check if any URLs are found
    contains_url = bool(urls)

    return contains_url, urls


# PROGRAM

# Initial prompt
messages_list = [SystemMessage(content=initial_system_prompt)]
initial_message = chat_model.invoke(messages_list)
print(f'\n {initial_message.content}')

# User input loop


while True:
    user_input = input("\nEnter input (type 'exit' to quit):\n")
    has_url, urls_list = find_urls(user_input)
    
    # Determine what type of input it is & act accordingly
    if user_input.lower() == 'exit':
        break
    
    ### TODO: Update URL detection to make more robust & account for urls / images over multiple user messages
    elif has_url == True:
        content = [ {"type": "text", "text": "Here are the images"}]
        for url in urls_list:
            url_dict = {
                "type": "image_url",
                "image_url": {
                    "url": url,
                    "detail": "auto",
                },
            }
            content.append(url_dict)
        print(f"debug: {content}")
        messages_list.append(HumanMessage(content=content))
        
    else:
        messages_list.append(HumanMessage(content=user_input))
    
    result = chat_model.invoke(messages_list)
    print(f"\n ============================")
    print(f"\n {result.content}")
    messages_list.append(SystemMessage(content=result.content))



