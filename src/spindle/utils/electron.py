import os
import subprocess
from spindle.exceptions import SpindleException

def run_electron_app():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    target_dir = os.path.join(script_dir, '..', '..', 'gui')

    if not os.path.exists(target_dir):
        raise SpindleException(f"The directory {target_dir} does not exist.")

    try:
        subprocess.run(['npm', '--version'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        raise SpindleException("NPM is not installed. Please install NPM and try again.")

    os.chdir(target_dir)

    try:
        print("Running 'npm install'... This might take a few minutes.")
        subprocess.run(['npm', 'install'], check=True)
        print("'npm install' completed successfully. Starting the Electron app with 'npm start'...")
        subprocess.run(['npm', 'start'], check=True)
    except subprocess.CalledProcessError as e:
        raise SpindleException(f"An error occurred while executing NPM commands: {e}")