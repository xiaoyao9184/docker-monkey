import os
import sys
import git
import subprocess
from huggingface_hub import snapshot_download

REPO_URL = os.getenv("REPO_URL", "https://github.com/Yuliang-Liu/MonkeyOCR.git")
REPO_BRANCH = os.getenv("REPO_BRANCH", "0c0c9458633e0cb4b6b471e38ec19254d4e80cf8")
LOCAL_PATH = os.getenv("LOCAL_PATH", "./MonkeyOCR")
MODEL_ID = os.getenv("MODEL_ID", "echo840/MonkeyOCR")

def install_src():
    if not os.path.exists(LOCAL_PATH):
        print(f"Cloning repository from {REPO_URL}...")
        repo = git.Repo.clone_from(REPO_URL, LOCAL_PATH)
        repo.git.checkout(REPO_BRANCH)
    else:
        print(f"Repository already exists at {LOCAL_PATH}")

    requirements_path = os.path.join(LOCAL_PATH, "requirements.txt")
    if os.path.exists(requirements_path):
        print("Installing requirements...")
        subprocess.check_call(["pip", "install", "-r", requirements_path])
    else:
        print("No requirements.txt found.")

def install_model():
    checkpoint_path = os.path.join(LOCAL_PATH, "model_weight")
    snapshot_download(repo_id=MODEL_ID, local_dir=checkpoint_path)

# clone repo and download model
install_src()
install_model()

# sys.path.append()
os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), LOCAL_PATH)))

# run gradio in subprocess in reloaded mode
# huggingface space issue: https://github.com/gradio-app/gradio/issues/10048
# need disable reload for huggingface space
import re
import sys
from gradio.cli import cli
if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.argv.append(re.sub(r'app\.py$', 'demo/demo_gradio.py', sys.argv[0]))
    sys.exit(cli())
