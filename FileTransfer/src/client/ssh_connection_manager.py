"""
SSH 연결 관리 모듈
"""
import logging
import threading
from typing import Optional, Dict, Any
import paramiko
from pathlib import Path


class SSHConnectionManager:
    """SSH 연결 관리 클래스"""
    
    def __init__(self):
        self.client: Optional[paramiko.SSHClient] = None
        self.sftp: Optional[paramiko.SFTPClient] = None
        self.connection_info: Dict[str, Any] = {}
        self.lock = threading.Lock()
        self.logger = logging.getLogger(__name__)
    
    def establish_connection(self, host: str, port: int, username: str, password: str) -> bool:
        """SSH 연결 설정 (패스워드 인증만 지원)"""
        with self.lock:
            try:
                # 기존 연결이 있다면 종료
                self.close_connection()
                
                self.logger.info(f"Attempting SSH connection to {host}:{port} as {username}")
                
                # SSH 클라이언트 생성
                self.client = paramiko.SSHClient()
                self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                
                # 연결 파라미터 설정
                connect_params = {
                    'hostname': host,
                    'port': port,
                    'username': username,
                    'password': password,
                    'timeout': 10,  # 연결 타임아웃 단축
                    'auth_timeout': 10,  # 인증 타임아웃
                    'banner_timeout': 10,  # 배너 타임아웃
                    'look_for_keys': False,  # SSH 키 자동 검색 비활성화
                    'allow_agent': False,  # SSH Agent 사용 비활성화
                    'compress': True  # 압축 사용
                }
                
                self.logger.debug(f"Connection parameters: {connect_params}")
                
                # 패스워드 인증으로 연결
                self.client.connect(**connect_params)
                self.logger.info(f"SSH connection established to {host}:{port}")
                
                # SFTP 클라이언트 생성
                self.logger.debug("Creating SFTP client...")
                self.sftp = self.client.open_sftp()
                self.logger.info("SFTP client created successfully")
                
                # 연결 테스트 - 현재 디렉토리 확인
                try:
                    current_dir = self.sftp.getcwd()
                    if current_dir is None:
                        current_dir = self.sftp.normalize('.')
                    self.logger.info(f"SFTP working directory: {current_dir}")
                except Exception as sftp_test_error:
                    self.logger.warning(f"SFTP test failed: {sftp_test_error}")
                
                # 연결 정보 저장
                self.connection_info = {
                    'host': host,
                    'port': port,
                    'username': username,
                    'auth_method': 'password'
                }
                
                self.logger.info(f"Successfully connected to {host}:{port}")
                return True
                
            except paramiko.AuthenticationException as e:
                self.logger.error(f"SSH authentication failed: {e}")
                return False
            except paramiko.SSHException as e:
                self.logger.error(f"SSH protocol error: {e}")
                return False
            except paramiko.ssh_exception.NoValidConnectionsError as e:
                self.logger.error(f"No valid SSH connections available: {e}")
                return False
            except ConnectionRefusedError as e:
                self.logger.error(f"Connection refused by server: {e}")
                return False
            except TimeoutError as e:
                self.logger.error(f"Connection timeout: {e}")
                return False
            except OSError as e:
                self.logger.error(f"Network error: {e}")
                return False
            except Exception as e:
                self.logger.error(f"Unexpected connection error: {e}")
                import traceback
                self.logger.debug(f"Full traceback: {traceback.format_exc()}")
                return False
    
    def close_connection(self):
        """SSH 연결 종료"""
        with self.lock:
            if self.sftp:
                try:
                    self.sftp.close()
                except Exception as e:
                    self.logger.warning(f"Error closing SFTP connection: {e}")
                finally:
                    self.sftp = None
            
            if self.client:
                try:
                    self.client.close()
                except Exception as e:
                    self.logger.warning(f"Error closing SSH connection: {e}")
                finally:
                    self.client = None
            
            self.connection_info = {}
            self.logger.info("SSH connection closed")
    
    def is_alive(self) -> bool:
        """연결 상태 확인"""
        if not self.client or not self.sftp:
            return False
        
        try:
            # 간단한 명령으로 연결 상태 확인
            transport = self.client.get_transport()
            if transport is None or not transport.is_active():
                return False
            
            # SFTP 연결도 확인
            self.sftp.listdir('.')
            return True
            
        except Exception:
            return False
    
    def get_connection_info(self) -> Dict[str, Any]:
        """연결 정보 반환"""
        return self.connection_info.copy()
    
    def execute_command(self, command: str) -> tuple:
        """원격 명령 실행"""
        if not self.client:
            raise RuntimeError("Not connected to SSH server")
        
        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            exit_code = stdout.channel.recv_exit_status()
            output = stdout.read().decode('utf-8')
            error = stderr.read().decode('utf-8')
            return exit_code, output, error
        except Exception as e:
            self.logger.error(f"Command execution failed: {e}")
            raise
    
    def get_sftp(self) -> paramiko.SFTPClient:
        """SFTP 클라이언트 반환"""
        if not self.sftp:
            raise RuntimeError("SFTP connection not established")
        return self.sftp
    
    def get_sftp_client(self) -> paramiko.SFTPClient:
        """SFTP 클라이언트 반환 (호환성을 위한 별칭)"""
        return self.get_sftp()
