#!/usr/bin/env python3
"""
최소한의 SSH 연결 테스트 - 가장 기본적인 paramiko 테스트
"""
import sys

def test_minimal_ssh():
    """가장 기본적인 SSH 연결 테스트"""
    try:
        import paramiko
        print(f"Paramiko 버전: {paramiko.__version__}")
        
        # 사용자 입력
        host = input("SSH 호스트: ")
        port = int(input("SSH 포트 (기본 22): ") or "22")
        username = input("사용자명: ")
        password = input("비밀번호: ")
        
        print(f"\n연결 시도: {username}@{host}:{port}")
        
        # 가장 기본적인 SSH 연결
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        print("SSH 연결 중...")
        client.connect(
            hostname=host,
            port=port,
            username=username,
            password=password,
            timeout=30
        )
        print("✅ SSH 연결 성공!")
        
        # 간단한 명령 실행
        print("명령 실행 테스트...")
        stdin, stdout, stderr = client.exec_command('whoami')
        result = stdout.read().decode().strip()
        print(f"현재 사용자: {result}")
        
        # SFTP 테스트
        print("SFTP 테스트...")
        sftp = client.open_sftp()
        files = sftp.listdir('.')
        print(f"파일 수: {len(files)}")
        
        sftp.close()
        client.close()
        
        print("✅ 모든 테스트 성공!")
        return True
        
    except ImportError:
        print("❌ paramiko 라이브러리가 설치되지 않았습니다.")
        print("설치: pip install paramiko")
        return False
        
    except paramiko.AuthenticationException:
        print("❌ 인증 실패 - 사용자명/비밀번호를 확인하세요")
        return False
        
    except paramiko.SSHException as e:
        print(f"❌ SSH 오류: {e}")
        return False
        
    except Exception as e:
        print(f"❌ 오류: {e}")
        import traceback
        print("상세 오류 정보:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("최소한의 SSH 연결 테스트")
    print("=" * 50)
    
    if test_minimal_ssh():
        print("\n🎉 SSH 연결이 정상적으로 작동합니다!")
    else:
        print("\n💥 SSH 연결에 문제가 있습니다.")
    
    input("\n아무 키나 누르세요...")