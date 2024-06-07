import os
import subprocess
import re
from groq import Groq
import webbrowser

system_prompt = """
you chould write streamlit code. you can not use images!!
The code should be funktional. you often get a small input, so try to add cool features and easter egg in this code you yould only write code you dont have to add comments.   a
nd the code should be working out of the box. if you have libarys to install say how to install them in the terminals section only run pip instal ...... 
you dont hafe to install streamlit. also add an titel in the title section.  nothing else in this setion (small and funny title). the scripts will be running on macos it should look like this :
when you get ask to generate some kind of informational (just information no ui) you can yuse the markdown funktion of streamlit and generate a nice page.
```title
your title
```
```python
your code
```
```terminal
pip install ......
```
"""



class LLM:
    def __init__(self, system_prompt, model="llama3-70b-8192"):
        self.model = model
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.history =  [{'role': 'system', 'content': system_prompt}]

    def message(self, user_message):
        self.history.append({'role': 'user', 'content': user_message})
        completion = self.client.chat.completions.create(
            messages=self.history,
            model=self.model
        )
        answer = completion.choices[0].message.content

        self.history.append({'role': 'assistant', 'content': answer})
        return answer



def start_server(port, name="app.py"):
    try:
        process = subprocess.Popen(
                    ["streamlit", "run", name, "--server.port", str(port)],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
        process.wait(1)
    except:
        pass

def create_site(name, script, path="pages/"):

    if not os.path.exists(path):
        os.makedirs(path)

    file_path = os.path.join(path, name + ".py")

    with open(file_path, "w") as file:
        file.write(script)


def convert_data(input_string):
    title_pattern = r'```title\n(.*?)\n```'
    script_pattern = r'```python\n(.*?)\n```'
    terminal_pattern = r'```terminal\n(.*?)\n```'

    title_match = re.search(title_pattern, input_string, re.DOTALL)
    script_match = re.search(script_pattern, input_string, re.DOTALL)
    terminal_match = re.search(terminal_pattern, input_string, re.DOTALL)

    title = title_match.group(1).strip() if title_match else None
    script = script_match.group(1).strip() if script_match else None
    terminalcommands = terminal_match.group(1).strip() if terminal_match else None

    return [title, script, terminalcommands]

def name_site(input_string, path="pages/"):
    lowercase_string = input_string.lower()
    transformed_string = lowercase_string.replace(" ", "_")
    filename = transformed_string + ".py"
    directory = path
    path = directory + filename
    count = 0

    while os.path.exists(path):
        count += 1
        filename = f"{transformed_string}{count}.py"
        path = directory + filename

    return filename[:-3]

def execute_commands(commands: str):
    command_list = commands.strip().split('\n')

    for command in command_list:
        try:
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return(result.stdout.decode())
        except subprocess.CalledProcessError as e:
            print("-----")
            print(e)


class Site:
    def __init__(self, port=4877):
        start_server(port)
        self.port = port
        self.site_history = LLM(system_prompt)

    def add_side(self, prompt):
        answer = self.site_history.message(prompt)
        list_answer = convert_data(answer)
        execute_commands(list_answer[2])
        if list_answer[0]:
            title = name_site(list_answer[0])
        else:
            title = name_site("Untitled")
        create_site(title, list_answer[1])
        print(self.port)
        return f"http://localhost:{self.port}/{title}"

def make_site(prompt):
    site = Site()

    user_message = prompt
    url = site.add_side(user_message)
    webbrowser.open(url)
    print(f"here is your Website: {url}")
if __name__ == "__main__":
    make_site("make a number guessing game")