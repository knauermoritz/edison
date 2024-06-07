# Edison

Edison is a personal assistant that facilitates natural interaction with your computer.

## Prerequisites
- Python needs to be installed on your system.

## Getting Started

1. Set up your GROQ API key:
   ```bash
   export GROQ_API_KEY=<your-api-key-here>
   ```
   You can obtain your API key by logging in at [GROQ Console](https://console.groq.com/login).

2. Clone the repository:
   ```bash
   git clone https://github.com/knauermoritz/edison.git
   cd edison
   ```

3. Create a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   ```

4. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```bash
     source venv/bin/activate
     ```

5. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

6. Start Edison:
   ```bash
   python3 edison.py
   ```

## Usage

Once Edison is running, you can interact with it using the keyword "**EDISON**". After receiving an answer, you can continue to interact with it without the keyword for the next 15 seconds.

Edison can execute terminal commands or Python code, create files, demonstrate functions, generate websites, provide information, and even generate PDFs. Explore its capabilities and enhance your productivity!

### Silence Mode
To activate silence mode, use the command:
```bash
python3 edison.py -silent
```
