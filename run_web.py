import os
import subprocess
import sys

from app.core.config import settings

if __name__ == "__main__":
    cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        "web/streamlit_app.py",
        "--server.port",
        str(settings.web_port),
    ]
    os.environ.setdefault("PYTHONPATH", os.getcwd())
    subprocess.run(cmd, check=True)
