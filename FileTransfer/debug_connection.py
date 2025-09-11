#!/usr/bin/env python3
"""
SSH 연결 디버깅 도구 - 단계별 연결 테스트
"""
import sys
import socket
import time
import traceback
from pathlib import Path

# Add the src directory to the Python path
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

def test_basic_connection():
    """기본 라이브러리 및 환경 테스트"""
    print("=" * 60)
    print("🔧 기본 환경 테스트")
    print("=" * 60)
    
    # Python 버전
    print(f"Python 버전: {sys.version}")
    
    # 필수 라이브러리 확인
    try:
        import paramiko
        print(f"✅ Paramiko 버전: {paramiko.__version__}")
    except ImportError as e:
        print(f"❌ Paramiko 설치 필요: {e}")
        return False
    
    try:
        from PySide6.QtCore import __version__ as qt_version
        print(f"✅ PySide6 버전: {qt_version}")
    except ImportError as e:
        print(f"❌ PySide6 설치 필요: {e}")
        return False
    
    return True

def test_tcp_connection(host, port, timeout=5):
    """TCP 연결 테스트"""
    print(f"\n🔗 TCP 연결 테스트: {host}:{port}")
    print("-" * 40)
    
    try:
        print(f"  • 소켓 생성 중...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        
        print(f"  • 연결 시도 중... (타임아웃: {timeout}초)")
        start_time = time.time()
        result = sock.connect_ex((host, port))
        end_time = time.time()
        
        sock.close()
        
        if result == 0:
            print(f"  ✅ TCP 연결 성공 ({end_time - start_time:.2f}초)")
            return True
        else:
            print(f"  ❌ TCP 연결 실패 (오류 코드: {result})")
            return False
            
    except socket.timeout:
        print(f"  ❌ 연결 타임아웃 ({timeout}초 초과)")
        return False
    except socket.gaierror as e:
        print(f"  ❌ 호스트명 해석 실패: {e}")
        return False
    except Exception as e:
        print(f"  ❌ TCP 연결 오류: {e}")
        return False

def test_ssh_handshake(host, port, timeout=10):
    """SSH 핸드셰이크 테스트"""
    print(f"\n🔐 SSH 핸드셰이크 테스트: {host}:{port}")
    print("-" * 40)
    
    try:
        import paramiko
        
        print("  • SSH 클라이언트 생성 중...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        print("  • SSH 핸드셰이크 시도 중...")
        start_time = time.time()
        
        # 연결만 시도 (인증은 하지 않음)
        transport = paramiko.Transport((host, port))
        transport.start_client(timeout=timeout)
        
        end_time = time.time()
        
        if transport.is_authenticated() is not None:  # 연결은 성공, 인증은 아직 안함
            remote_version = transport.remote_version
            print(f"  ✅ SSH 핸드셰이크 성공 ({end_time - start_time:.2f}초)")
            print(f"  📋 원격 SSH 버전: {remote_version}")
            
            # 지원되는 인증 방법 확인
            try:
                auth_methods = transport.auth_none('dummy')
                print(f"  🔑 지원되는 인증 방법: {auth_methods}")
            except paramiko.BadAuthenticationType as e:
                auth_methods = e.allowed_types
                print(f"  🔑 지원되는 인증 방법: {auth_methods}")
            except:
                print("  🔑 인증 방법 정보를 가져올 수 없습니다")
            
            transport.close()
            return True
        else:
            print("  ❌ SSH 핸드셰이크 실패")
            transport.close()
            return False
            
    except paramiko.SSHException as e:
        print(f"  ❌ SSH 프로토콜 오류: {e}")
        return False
    except socket.timeout:
        print(f"  ❌ SSH 핸드셰이크 타임아웃 ({timeout}초)")
        return False
    except Exception as e:
        print(f"  ❌ SSH 핸드셰이크 오류: {e}")
        print(f"  🔧 상세 오류: {traceback.format_exc()}")
        return False

def test_ssh_auth(host, port, username, password, timeout=10):
    """SSH 인증 테스트"""
    print(f"\n🔓 SSH 인증 테스트: {username}@{host}:{port}")
    print("-" * 40)
    
    try:
        import paramiko
        
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        print("  • SSH 인증 시도 중...")
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
        print(f"  ✅ SSH 인증 성공 ({end_time - start_time:.2f}초)")
        
        # 간단한 명령 실행 테스트
        try:
            print("  • 명령 실행 테스트 중...")
            stdin, stdout, stderr = client.exec_command('echo "Hello SSH"', timeout=5)
            output = stdout.read().decode().strip()
            if output == "Hello SSH":
                print("  ✅ SSH 명령 실행 성공")
            else:
                print(f"  ⚠️  SSH 명령 실행 결과 이상: {output}")
        except Exception as cmd_error:
            print(f"  ⚠️  SSH 명령 실행 실패: {cmd_error}")
        
        client.close()
        return True
        
    except paramiko.AuthenticationException as e:
        print(f"  ❌ SSH 인증 실패: 사용자명/비밀번호 확인")
        return False
    except paramiko.SSHException as e:
        print(f"  ❌ SSH 연결 오류: {e}")
        return False
    except Exception as e:
        print(f"  ❌ SSH 인증 테스트 오류: {e}")
        return False

def test_sftp_connection(host, port, username, password, timeout=10):
    """SFTP 연결 테스트"""
    print(f"\n📁 SFTP 연결 테스트: {username}@{host}:{port}")
    print("-" * 40)
    
    try:
        import paramiko
        
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        print("  • SSH 연결 중...")
        client.connect(
            hostname=host,
            port=port,
            username=username,
            password=password,
            timeout=timeout,
            look_for_keys=False,
            allow_agent=False
        )
        
        print("  • SFTP 세션 생성 중...")
        sftp = client.open_sftp()
        
        print("  • SFTP 기능 테스트 중...")
        
        # 현재 디렉토리 확인
        current_dir = sftp.getcwd()
        if current_dir is None:
            current_dir = sftp.normalize('.')
        print(f"  📂 현재 디렉토리: {current_dir}")
        
        # 파일 목록 조회
        files = sftp.listdir('.')
        print(f"  📋 파일/폴더 수: {len(files)}개")
        
        if files:
            print("  📄 처음 5개 항목:")
            for i, file in enumerate(files[:5]):
                print(f"    {i+1}. {file}")
        
        print("  ✅ SFTP 연결 및 기능 테스트 성공")
        
        sftp.close()
        client.close()
        return True
        
    except Exception as e:
        print(f"  ❌ SFTP 연결 테스트 실패: {e}")
        return False

def main():
    """메인 디버깅 함수"""
    print("🔍 SSH 연결 디버깅 도구")
    print("이 도구는 SSH 연결 문제를 단계별로 진단합니다.")
    print()
    
    # 1. 기본 환경 테스트
    if not test_basic_connection():
        print("\n❌ 기본 환경 테스트 실패. 필수 라이브러리를 설치하세요.")
        return 1
    
    # 2. 사용자 입력
    print("\n" + "=" * 60)
    print("📝 SSH 서버 정보 입력")
    print("=" * 60)
    
    host = input("호스트 주소: ").strip()
    if not host:
        print("❌ 호스트 주소를 입력해야 합니다.")
        return 1
    
    try:
        port = int(input("포트 (기본 22): ").strip() or "22")
    except ValueError:
        print("❌ 올바른 포트 번호를 입력하세요.")
        return 1
    
    username = input("사용자명: ").strip()
    if not username:
        print("❌ 사용자명을 입력해야 합니다.")
        return 1
    
    password = input("비밀번호: ").strip()
    if not password:
        print("❌ 비밀번호를 입력해야 합니다.")
        return 1
    
    # 3. 단계별 테스트 실행
    print("\n" + "=" * 60)
    print("🚀 연결 테스트 시작")
    print("=" * 60)
    
    # TCP 연결 테스트
    tcp_success = test_tcp_connection(host, port)
    
    if tcp_success:
        # SSH 핸드셰이크 테스트
        ssh_handshake_success = test_ssh_handshake(host, port)
        
        if ssh_handshake_success:
            # SSH 인증 테스트
            auth_success = test_ssh_auth(host, port, username, password)
            
            if auth_success:
                # SFTP 테스트
                sftp_success = test_sftp_connection(host, port, username, password)
                
                if sftp_success:
                    print(f"\n🎉 모든 테스트 통과! SSH/SFTP 연결이 정상입니다.")
                    return 0
    
    print(f"\n💡 문제 해결 가이드:")
    print(f"  • TCP 연결 실패: 서버 주소, 포트, 방화벽 설정 확인")
    print(f"  • SSH 핸드셰이크 실패: SSH 서비스 상태 확인")
    print(f"  • SSH 인증 실패: 사용자명/비밀번호 확인")
    print(f"  • SFTP 연결 실패: SFTP 서비스 활성화 확인")
    
    return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  사용자에 의해 중단되었습니다.")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 예상치 못한 오류: {e}")
        print(f"🔧 상세 정보:\n{traceback.format_exc()}")
        sys.exit(1)