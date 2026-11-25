import subprocess
import time
from pathlib import Path

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
BASE_DIR = Path(r"C:\Unimate_AI_Assisstanat")
OUT_DIR = BASE_DIR / "Academic_Documents" / "screenshots"
OUT_DIR.mkdir(parents=True, exist_ok=True)

pages = [
    ("screenshot_1_dashboard.png", "dashboard"),
    ("screenshot_2_documents.png", "documents"),
    ("screenshot_3_chatbot.png", "chat"),
    ("screenshot_4_summarizer.png", "summarizer"),
    ("screenshot_5_quiz.png", "quiz"),
    ("screenshot_6_study_planner.png", "study_planner"),
    ("screenshot_7_analytics.png", "analytics"),
    ("screenshot_8_genai_concepts.png", "genai_concepts"),
]

for filename, page_name in pages:
    out_file = OUT_DIR / filename
    url = f"http://127.0.0.1:8000/?page={page_name}"
    print(f"Capturing {page_name} -> {filename}...")
    
    cmd = [
        CHROME_PATH,
        "--headless",
        "--disable-gpu",
        f"--screenshot={str(out_file)}",
        "--window-size=1280,850",
        "--virtual-time-budget=3000",
        url
    ]
    subprocess.run(cmd, check=True)
    time.sleep(0.5)

print("All screenshots captured successfully!")
