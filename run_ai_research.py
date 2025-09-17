# run_ai_research.py
"""Easy launcher for AI Research Tool"""

import subprocess
import sys
import os

# def install_requirements():
#     """Install required packages"""
#     print(" Installing required packages...")
#     try:
#         subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
#         print(" Requirements installed successfully!")
#         return True
#     except subprocess.CalledProcessError as e:
#         print(f" Failed to install requirements: {e}")
#         return False

def run_streamlit_app():
    """Run the Streamlit application"""
    print(" Starting AI Research Tool...")
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "main.py", "--server.port", "8501", "--server.address", "localhost"])
    except KeyboardInterrupt:
        print("\n AI Research Tool stopped by user")
    except Exception as e:
        print(f" Failed to start application: {e}")

def main():
    """Main launcher function"""
    print(" AI Research Tool Launcher")
    print("=" * 40)
    
    # Check if requirements.txt exists
    if not os.path.exists("requirements.txt"):
        print(" requirements.txt not found!")
        return
    
    # # Install requirements
    # if not install_requirements():
    #     return
    
    # Run the app
    run_streamlit_app()

if __name__ == "__main__":
    main()
