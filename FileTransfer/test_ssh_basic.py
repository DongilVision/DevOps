#!/usr/bin/env python3
"""
기본 SSH 연결 테스트 - 비대화형 버전
"""
import sys
import os
import traceback

def test_paramiko_installation():
    """Paramiko 설치 및 버전 확인"""
    try:
        import paramiko
        print(f"Paramiko version: {paramiko.__version__}")
        return True
    except ImportError as e:
        print(f"ERROR: Paramiko not installed - {e}")
        return False

def test_pyside6_installation():
    """PySide6 설치 및 버전 확인"""
    try:
        from PySide6.QtCore import __version__ as qt_version
        print(f"PySide6 version: {qt_version}")
        return True
    except ImportError as e:
        print(f"ERROR: PySide6 not installed - {e}")
        return False

def test_imports():
    """필수 모듈 import 테스트"""
    try:
        # src 디렉토리 추가
        from pathlib import Path
        src_dir = Path(__file__).parent / "src"
        if str(src_dir) not in sys.path:
            sys.path.insert(0, str(src_dir))
        
        print("Testing imports...")
        
        # SSH 연결 관리자 import
        from client.ssh_connection_manager import SSHConnectionManager
        print("OK - SSH Connection Manager imported")
        
        # 간단한 테스트 GUI import
        from client.simple_test_gui import SimpleTestGUI
        print("OK - Simple Test GUI imported")
        
        return True
    except Exception as e:
        print(f"ERROR: Import failed - {e}")
        traceback.print_exc()
        return False

def main():
    print("=" * 60)
    print("Basic SSH Environment Test")
    print("=" * 60)
    
    success = True
    
    # 1. Paramiko 확인
    print("\n1. Testing Paramiko installation...")
    if not test_paramiko_installation():
        success = False
    
    # 2. PySide6 확인
    print("\n2. Testing PySide6 installation...")
    if not test_pyside6_installation():
        success = False
    
    # 3. 모듈 import 확인
    print("\n3. Testing module imports...")
    if not test_imports():
        success = False
    
    print("\n" + "=" * 60)
    if success:
        print("OK - All basic tests passed!")
        print("Environment is ready for SSH testing.")
        
        print("\nNext steps:")
        print("1. Run: python test_connection.py")
        print("2. Or run: python debug_connection.py")
        
        return 0
    else:
        print("ERROR - Some tests failed!")
        print("Please install missing dependencies:")
        print("  pip install paramiko PySide6")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        traceback.print_exc()
        sys.exit(1)