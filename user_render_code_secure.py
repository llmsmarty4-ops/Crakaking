import os
import uuid
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "7951330550:AAFAmO0k8NtcUL9pbqR0x2HdV9UELVAQ09E"

# ================== DOCKER SECURITY ==================
def ensure_docker_image():
    subprocess.run(
        ["docker", "pull", "python:3.11-slim"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

def run_user_code_in_sandbox(user_id: int, user_code_path: str):
    ensure_docker_image()
    container_name = f"user_{user_id}_{uuid.uuid4().hex[:8]}"
    docker_cmd = [
        "docker", "run",
        "--rm",
        "--name", container_name,
        "--network", "none",
        "--read-only",
        "--cap-drop=ALL",
        "--security-opt", "no-new-privileges",
        "--security-opt", "seccomp=default",
        "--pids-limit", "64",
        "--memory", "256m",
        "-v", f"{user_code_path}:/app/main.py:ro",
        "python:3.11-slim", "python", "/app/main.py"
    ]
    subprocess.Popen(docker_cmd)

# ================== END DOCKER SECURITY ==================

# ... (Your original code continues here)

# Example of how to use this:
# Instead of directly running user code, call run_user_code_in_sandbox(user_id, user_code_path)
