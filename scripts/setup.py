import os
from dotenv import load_dotenv

load_dotenv()

print("Gurt Setup")
Token = input("Token: ")
BrowserPath = input("Browser Path: ")
TempPath = input("Temp Path: ")

path = os.path.join(os.path.dirname(__file__), "..", ".env")

with open(path, "w") as f:
    f.write(f"TOKEN={Token}\n")
    f.write(f"CHROME_PATH={BrowserPath}\n")
    f.write(f"DEBUG_PROFILE={TempPath}\n")