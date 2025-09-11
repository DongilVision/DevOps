#!/usr/bin/env python3
"""
SSH 접속 테스트 실행 스크립트
"""
import sys
import os
from pathlib import Path

# Add the src directory to the Python path
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

def main():
    """SSH 접속 테스트 GUI 실행"""
    try:
        from src.client.simple_test_gui import main as run_test_gui
        
        print("SSH 접속 테스트 GUI를 시작합니다...")
        return run_test_gui()
        
    except ImportError as e:
        print(f"Import error: {e}")
        print("Required packages:")
        print("  pip install PySide6 paramiko")
        return 1
    except Exception as e:
        print(f"Error starting test GUI: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())