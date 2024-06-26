import contextlib
import time
from threading import Timer
from execute import *
from llm import LLM
from tts import generate_voice
from prompt import system_prompt
from website import make_site
import sys
with contextlib.redirect_stdout(None):
    from RealtimeSTT import AudioToTextRecorder


chat = LLM(system_prompt)

def print_question(text):
    BOLD = '\033[1m'
    ITALIC = '\033[3m'
    RESET = '\033[0m'  
    print(f"{BOLD}{ITALIC}{text}{RESET}")

def print_answer(text):
    lines = text.split('\n')
    non_empty_lines = [line for line in lines if line.strip() != '']
    cleaned_text = '\n'.join(non_empty_lines)
    if cleaned_text:
        GREY = '\033[90m'
        RESET = '\033[0m'
        print(f"{GREY}{cleaned_text}{RESET}")

def handle_answer(answer):
    try:
        answer, output = process(answer)
        answer = execute_functions(["make_site"], answer)
    except Exception as e:
        print(f"Error processing answer: {e}")
        output = None
    return answer, output

def main():
    silent_mode = '-silent' in sys.argv
    if silent_mode:
        while True:
            BOLD = '\033[1m'
            ITALIC = '\033[3m'
            RESET = '\033[0m'
            user_input = input(f"{BOLD}{ITALIC}>{RESET}{BOLD}{ITALIC}").strip()
            print('\033[F\033[K', end='')
            print_question(user_input)

            answer = chat.message(user_input)

            answer, output = handle_answer(answer)
            print_answer(answer)

            while output:
                prompt = f"here is the output can you please repeat it if there is no output just respond with . {output}"
                
                answer = chat.message(prompt)
                answer, output = handle_answer(answer)
                print_answer(answer)
    else:
        recorder = AudioToTextRecorder(spinner=False, model="base", language="en")
        keywords = ["ediren", "edi", "edidon", "edilin", "edimon", "edikin", "ediron", "edisona", "edisone", "edisong", "edisoni", "edisont", "edisonu", "edirin", "ediran", "ediren", "edisin", "edisun", "edisonic", "edisonio", "edisonee", "edion", "edisonator", "edister", "edilan", "edikin", "ediron", "edisene", "edisot", "edidon", "edize"]

        last_time = time.time()
        prompt_message = "say something..."
        print(f'\033[37m\033[2m{prompt_message}\033[0m', end='', flush=True)
        generate_voice(prompt_message)
    
        while True:
            rec = recorder.text()
            if any(keyword in rec.lower() for keyword in keywords) or ((time.time() - last_time) < 10):
                print('\r' + ' ' * len(prompt_message) + '\r', end='', flush=True)
                print_question(rec)
                answer = chat.message(rec)

                answer, output = handle_answer(answer)
                print_answer(answer)
                
                generate_voice(answer)
                print(f'\033[37m\033[2m{prompt_message}\033[0m', end='', flush=True)  

                while output:
                    prompt = f"here is the output can you please repeat it if there is no output just respond with . {output}"
                    
                    answer = chat.message(prompt)
                    answer, output = handle_answer(answer)
                    print_answer(answer)
                    generate_voice(answer)
                
                last_time = time.time()

if __name__ == '__main__':
    main()