#!/usr/bin/env python3
"""
SSH File Transfer Client Runner
SSH 파일 전송 클라이언트 실행 스크립트
"""

import sys
import os
from pathlib import Path

# Add the src directory to the Python path
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

def main():
    """Run the SSH file transfer client"""
    try:
        from client.ssh_client_ui import main as run_ssh_client
        
        # Run the SSH client UI
        return run_ssh_client()
        
    except ImportError as e:
        print(f"Import error: {e}")
        print("Please make sure all dependencies are installed:")
        print("pip install -r requirements.txt")
        print("Required packages: PySide6, paramiko")
        return 1
    except Exception as e:
        print(f"Error starting SSH client: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())