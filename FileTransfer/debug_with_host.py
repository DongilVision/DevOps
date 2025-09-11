#!/usr/bin/env python3
"""
SSH 연결 디버깅 도구 - host.json 사용, Windows 호환
"""
import sys
import socket
import time
import json
import traceback
from pathlib import Path

# Add the src directory to the Python path
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

def load_host_config():
    """host.json 파일에서 호스트 정보 로드"""
    try:
        host_file = Path(__file__).parent / "host.json"
        with open(host_file, 'r', encoding='utf-8') as f:
            hosts = json.load(f)
        return hosts[0] if hosts else None
    except Exception as e:
        print(f"ERROR: Failed to load host.json - {e}")
        return None

def test_basic_environment():
    """기본 라이브러리 및 환경 테스트"""
    print("=" * 60)
    print("Basic Environment Test")
    print("=" * 60)
    
    # Python 버전
    print(f"Python version: {sys.version}")
    
    # 필수 라이브러리 확인
    try:
        import paramiko
        print(f"OK - Paramiko version: {paramiko.__version__}")
    except ImportError as e:
        print(f"ERROR - Paramiko installation required: {e}")
        return False
    
    try:
        from PySide6.QtCore import __version__ as qt_version
        print(f"OK - PySide6 version: {qt_version}")
    except ImportError as e:
        print(f"ERROR - PySide6 installation required: {e}")
        return False
    
    return True

def test_tcp_connection(host, port, timeout=5):
    """TCP 연결 테스트"""
    print(f"\nStep 1: TCP Connection Test - {host}:{port}")
    print("-" * 50)
    
    try:
        print("  Creating socket...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        
        print(f"  Connecting to {host}:{port} (timeout: {timeout}s)...")
        start_time = time.time()
        result = sock.connect_ex((host, port))
        end_time = time.time()
        
        sock.close()
        
        if result == 0:
            print(f"  SUCCESS: TCP connection established ({end_time - start_time:.2f}s)")
            return True
        else:
            print(f"  FAILED: TCP connection failed (error code: {result})")
            print(f"    Troubleshooting:")
            print(f"    - Check if server is running on {host}:{port}")
            print(f"    - Check firewall settings")
            print(f"    - Verify host address and port number")
            return False
            
    except socket.timeout:
        print(f"  FAILED: Connection timeout ({timeout}s)")
        print(f"    Troubleshooting:")
        print(f"    - Server may be unreachable")
        print(f"    - Network connectivity issues")
        return False
    except socket.gaierror as e:
        print(f"  FAILED: Name resolution failed - {e}")
        print(f"    Troubleshooting:")
        print(f"    - Check host address spelling")
        print(f"    - DNS resolution issues")
        return False
    except Exception as e:
        print(f"  FAILED: TCP connection error - {e}")
        return False

def test_ssh_handshake(host, port, timeout=10):
    """SSH 핸드셰이크 테스트"""
    print(f"\nStep 2: SSH Handshake Test - {host}:{port}")
    print("-" * 50)
    
    try:
        import paramiko
        
        print("  Creating SSH transport...")
        start_time = time.time()
        
        # SSH Transport 생성 및 핸드셰이크
        transport = paramiko.Transport((host, port))
        transport.start_client(timeout=timeout)
        
        end_time = time.time()
        
        if transport.is_authenticated() is not None:  # 연결 성공, 인증은 아직 안함
            remote_version = transport.remote_version
            print(f"  SUCCESS: SSH handshake completed ({end_time - start_time:.2f}s)")
            print(f"  Remote SSH version: {remote_version}")
            
            # 지원되는 인증 방법 확인
            try:
                auth_methods = transport.auth_none('dummy')
                print(f"  Supported auth methods: {auth_methods}")
            except paramiko.BadAuthenticationType as e:
                auth_methods = e.allowed_types
                print(f"  Supported auth methods: {auth_methods}")
            except:
                print("  Auth methods: (unable to determine)")
            
            transport.close()
            return True
        else:
            print("  FAILED: SSH handshake failed")
            transport.close()
            return False
            
    except paramiko.SSHException as e:
        print(f"  FAILED: SSH protocol error - {e}")
        print(f"    Troubleshooting:")
        print(f"    - SSH service may not be running")
        print(f"    - Incorrect SSH port")
        return False
    except socket.timeout:
        print(f"  FAILED: SSH handshake timeout ({timeout}s)")
        print(f"    Troubleshooting:")
        print(f"    - SSH service response too slow")
        print(f"    - Network latency issues")
        return False
    except Exception as e:
        print(f"  FAILED: SSH handshake error - {e}")
        print(f"    Debug info: {traceback.format_exc()}")
        return False

def test_ssh_authentication(host, port, username, password, timeout=10):
    """SSH 인증 테스트"""
    print(f"\nStep 3: SSH Authentication Test - {username}@{host}:{port}")
    print("-" * 50)
    
    try:
        import paramiko
        
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        print("  Attempting SSH authentication...")
        start_time = time.time()
        
        client.connect(
            hostname=host,
            port=port,
            username=username,
            password=password,
            timeout=timeout,
            look_for_keys=False,
            allow_agent=False
        )
        
        end_time = time.time()
        print(f"  SUCCESS: SSH authentication successful ({end_time - start_time:.2f}s)")
        
        # 간단한 명령 실행 테스트
        try:
            print("  Testing command execution...")
            stdin, stdout, stderr = client.exec_command('echo "SSH command test"', timeout=5)
            output = stdout.read().decode().strip()
            if output == "SSH command test":
                print("  SUCCESS: SSH command execution works")
            else:
                print(f"  WARNING: Unexpected command output: {output}")
        except Exception as cmd_error:
            print(f"  WARNING: SSH command execution failed - {cmd_error}")
        
        client.close()
        return True
        
    except paramiko.AuthenticationException:
        print(f"  FAILED: SSH authentication failed")
        print(f"    Troubleshooting:")
        print(f"    - Check username: {username}")
        print(f"    - Check password")
        print(f"    - User may not have SSH access")
        return False
    except paramiko.SSHException as e:
        print(f"  FAILED: SSH connection error - {e}")
        return False
    except Exception as e:
        print(f"  FAILED: SSH authentication error - {e}")
        return False

def test_sftp_functionality(host, port, username, password, timeout=10):
    """SFTP 기능 테스트"""
    print(f"\nStep 4: SFTP Functionality Test - {username}@{host}:{port}")
    print("-" * 50)
    
    try:
        import paramiko
        
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        print("  Connecting via SSH...")
        client.connect(
            hostname=host,
            port=port,
            username=username,
            password=password,
            timeout=timeout,
            look_for_keys=False,
            allow_agent=False
        )
        
        print("  Opening SFTP session...")
        sftp = client.open_sftp()
        
        print("  Testing SFTP operations...")
        
        # 현재 디렉토리 확인
        current_dir = sftp.getcwd()
        if current_dir is None:
            current_dir = sftp.normalize('.')
        print(f"  Working directory: {current_dir}")
        
        # 파일 목록 조회
        files = sftp.listdir('.')
        print(f"  Files/folders count: {len(files)}")
        
        if files:
            print("  Directory contents (first 5 items):")
            for i, file in enumerate(files[:5]):
                print(f"    {i+1}. {file}")
            if len(files) > 5:
                print(f"    ... and {len(files) - 5} more items")
        
        print("  SUCCESS: SFTP functionality works correctly")
        
        sftp.close()
        client.close()
        return True
        
    except Exception as e:
        print(f"  FAILED: SFTP functionality error - {e}")
        print(f"    Troubleshooting:")
        print(f"    - SFTP subsystem may not be enabled")
        print(f"    - User may not have file access permissions")
        return False

def main():
    """메인 디버깅 함수"""
    print("SSH Connection Debugging Tool")
    print("This tool diagnoses SSH connection issues step by step.")
    print()
    
    # 1. 기본 환경 테스트
    if not test_basic_environment():
        print("\nERROR: Basic environment test failed.")
        print("Please install required libraries: pip install paramiko PySide6")
        return 1
    
    # 2. host.json 로드
    host_config = load_host_config()
    if not host_config:
        print("\nERROR: Cannot load host configuration from host.json")
        return 1
    
    host = host_config['host']
    port = host_config['port']
    username = host_config['username']
    password = host_config['password']
    
    print(f"\n" + "=" * 60)
    print(f"Testing SSH Connection")
    print(f"Target: {username}@{host}:{port}")
    print("=" * 60)
    
    # 3. 단계별 테스트 실행
    tcp_success = test_tcp_connection(host, port)
    
    if tcp_success:
        ssh_handshake_success = test_ssh_handshake(host, port)
        
        if ssh_handshake_success:
            auth_success = test_ssh_authentication(host, port, username, password)
            
            if auth_success:
                sftp_success = test_sftp_functionality(host, port, username, password)
                
                if sftp_success:
                    print(f"\n" + "=" * 60)
                    print("SUCCESS: All tests passed!")
                    print("SSH/SFTP connection is working perfectly.")
                    print("=" * 60)
                    return 0
    
    print(f"\n" + "=" * 60)
    print("Troubleshooting Guide:")
    print("- TCP connection failed: Check server address, port, firewall")
    print("- SSH handshake failed: Check SSH service status")
    print("- SSH authentication failed: Check username/password")
    print("- SFTP functionality failed: Check SFTP service configuration")
    print("=" * 60)
    
    return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nDebugging interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        print(f"Full traceback:\n{traceback.format_exc()}")
        sys.exit(1)