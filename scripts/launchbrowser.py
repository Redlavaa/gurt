import subprocess
from dotenv import load_dotenv
import os

load_dotenv()

def launch_browser():
    subprocess.Popen([
        os.getenv("BROWSER_PATH"),
        "--remote-debugging-port=9222",
        f"--user-data-dir={os.getenv('TEMP_PATH')}"
    ])

launch_browser()