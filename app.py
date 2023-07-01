import os
from dotenv import load_dotenv
load_dotenv()
import openai
import gradio

openai.api_key = os.getenv("OPENAI_API_KEY")

messages = [
    {"role": "system", "content": "You are a Competitive Programming expert that specializes in coding and Competitive Data structures and Algorithms"}
]

def count_tokens(messages):
    total_tokens = 0
    for message in messages:
        content = message.get("content", "")
        tokens = len(content.split())
        total_tokens += tokens
    return total_tokens

def truncate_messages(messages, max_tokens):
    while count_tokens(messages) > max_tokens:
        messages.pop(0)

def CustomChatGPT(user_input):
    messages.append({"role": "user", "content": user_input})
    max_tokens = 4096  # Maximum token limit for GPT-3.5 Turbo model
    truncate_messages(messages, max_tokens)
    
    # Truncate the last message if it exceeds the limit
    if count_tokens(messages) > max_tokens:
        last_message = messages[-1]
        last_message_content = last_message.get("content", "")
        last_message_tokens = len(last_message_content.split())
        excess_tokens = count_tokens(messages) - max_tokens
        truncated_content = " ".join(last_message_content.split()[:-excess_tokens])
        last_message["content"] = truncated_content
    
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    ChatGPT_reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": ChatGPT_reply})

    return ChatGPT_reply

demo = gradio.Interface(
    fn=CustomChatGPT,
    inputs="text",
    outputs="text",
    title="CodeGPT",
    description="CodeGPT is a GPT-3.5 Turbo-based coding assistant for general programming jobs, data structures, algorithms, and competitive programming. You can extract text responses to coding-related prompts using this model.Using OpenAI's potent GPT-3.5 Turbo model, CodeGPT was created. We would like to thank OpenAI for their contributions to the machine learning and natural language processing fields."
)

demo.launch()
