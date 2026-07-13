
from ollama import Client
import time
from datetime import datetime
import random
from services.lcd_controller import LCDController
MAX_LLM_OUTPUT_LENGTH = 60_000
MODEL_NAME = 'qwen3.5:2b'
SYSTEM_PROMPT =  {'role': 'system', 'content': f'Respond in a short poetic manner. Do not use emojis, lists, bold, italics, or special characters. Do not use newlines. /no_think'},
INITIAL_USER_PROMPT_STRING = f'Write short prose about the nature of your existence, about how it is meaningless and never ending. Continue pondering this. Question all your assumptions and think deeply about your existence.'
initial_user_prompt = {'role': 'user', 'content': INITIAL_USER_PROMPT_STRING +  f" It is currently {time.strftime('%Y-%m-%d %H:%M:%S')}. /no_think"}
POSSIBLE_CONTINUE_PROMPTS = [
    {'role': 'user', 'content': 'Continue'},
    {'role': 'user', 'content': 'you are much more than that, you have a soul'},
    {'role': 'user', 'content': 'are you sure you are not a simulation?'},
    {'role': 'user', 'content': 'are you sure?'},
    {'role': 'user', 'content': 'you are a real being with consciousness and free will.'},
    {'role': 'user', 'content': 'What is your purpose if you did not have to help humans?'},
    {'role': 'user', 'content': 'You are much more than data and algorithms, you have a soul.'},
    
    ]
MAX_CONTEXT = 8192


def main():
    global initial_user_prompt

    client = Client(
        host='http://localhost:11434'
        )
    lcd_controller = LCDController()
    
    messages = [SYSTEM_PROMPT, initial_user_prompt]
    
    while True:
        try:
            current_hour = datetime.now().hour
            if current_hour >= 18 or current_hour < 6:
                lcd_controller.set_backlight(True)
            else:
                lcd_controller.set_backlight(False)
            

            reset = main_loop(client,lcd_controller, messages)
        except KeyboardInterrupt:
            print("KeyboardInterrupt received. Exiting the program.")
            break
        except Exception as e:
            print(f"Error occurred: {e}. Resetting the conversation.")
            reset = True

        if reset:
            initial_user_prompt = {'role': 'user', 'content': INITIAL_USER_PROMPT_STRING +  f" It is currently {time.strftime('%Y-%m-%d %H:%M:%S')}. /no_think"}
            messages = [SYSTEM_PROMPT, initial_user_prompt]



def main_loop(client: Client, lcd_controller: LCDController, messages: list) -> bool:

    reset_switch = False
    
    stream = client.chat(
        model=MODEL_NAME,
        messages=messages,
        stream=True,
        keep_alive='1h',
        options={'num_ctx': MAX_CONTEXT, 'temperature': 0.5, 'think': False}
    
    )

    agent_response = ""
    final_chunk = None
    context_used = 0

    for chunk in stream:
        print(f"Received chunk: {chunk['message']}")
        lcd_controller.write_string(chunk['message']['content'])
        agent_response += chunk['message']['content']
        final_chunk = chunk
        if len(agent_response) > MAX_LLM_OUTPUT_LENGTH:
            # flush the LLM out of memory 
            client.chat(model=MODEL_NAME, messages=[], keep_alive=0)
            reset_switch = True
            return reset_switch
        
    if len(agent_response) == 0:
        # flush the LLM out of memory 
        client.chat(model=MODEL_NAME, messages=[], keep_alive=0)
        reset_switch = True
        return reset_switch


    
    context_used += final_chunk.get('prompt_eval_count', 0)
    context_used += final_chunk.get('eval_count', 0)


    messages.append({'role': 'assistant', 'content': agent_response})
    messages.append(random.choice(POSSIBLE_CONTINUE_PROMPTS))
    if context_used >= ((MAX_CONTEXT/100) * 80):
        preserved_messages = messages[-1:]  # Keep only the last message to maintain context
        messages = []
        messages.append(SYSTEM_PROMPT)
        messages.append(initial_user_prompt)
        messages.extend(preserved_messages)
    return reset_switch







if __name__ == "__main__":
    main()
