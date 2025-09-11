import logging
import threading
from pathlib import Path
from typing import Optional, List, Callable

from .ssh_connection_manager import SSHConnectionManager
from .sftp_file_browser import SFTPFileBrowser, SFTPFileInfo
from src.common.file_info import FileInfo


class SSHFileTransferClient:
    """SSH/SFTP 기반 파일 전송 클라이언트"""
    
    def __init__(self):
        self.ssh_manager = SSHConnectionManager()
        self.file_browser = SFTPFileBrowser(self.ssh_manager)
        self.is_connected = False
        self.current_transfer = None
        self.transfer_lock = threading.Lock()
        self.logger = logging.getLogger(__name__)
    
    def connect(self, host: str, port: int, username: str, password: str) -> bool:
        """SSH 서버에 연결"""
        try:
            success = self.ssh_manager.establish_connection(
                host=host,
                port=port, 
                username=username,
                password=password
            )
            
            if success:
                self.is_connected = True
                self.file_browser.refresh_local()
                self.file_browser.refresh_remote()
                self.logger.info(f"Connected to SSH server {host}:{port}")
            
            return success
        except Exception as e:
            self.logger.error(f"Connection failed: {e}")
            return False
    
    def disconnect(self):
        """SSH 연결 종료"""
        self.ssh_manager.close_connection()
        self.is_connected = False
        self.logger.info("Disconnected from SSH server")
    
    def get_local_files(self) -> List[FileInfo]:
        """로컬 파일 목록 조회"""
        return self.file_browser.local_files
    
    def get_remote_files(self) -> List[SFTPFileInfo]:
        """원격 파일 목록 조회"""
        return self.file_browser.remote_files
    
    def navigate_local(self, path: Path):
        """로컬 디렉토리 이동"""
        self.file_browser.navigate_to_local(path)
    
    def navigate_remote(self, path: str):
        """원격 디렉토리 이동"""
        self.file_browser.navigate_to_remote(path)
    
    def upload_file(self, local_file_name: str, progress_callback: Callable = None) -> bool:
        """파일 업로드"""
        if not self.is_connected:
            self.logger.error("Not connected to SSH server")
            return False
        
        local_file = self.file_browser.get_local_file_by_name(local_file_name)
        if not local_file:
            self.logger.error(f"Local file not found: {local_file_name}")
            return False
        
        if local_file.is_directory:
            self.logger.error("Directory upload not supported yet")
            return False
        
        with self.transfer_lock:
            self.current_transfer = f"Uploading {local_file_name}"
            success = self.file_browser.upload_file(local_file, progress_callback)
            self.current_transfer = None
        
        return success
    
    def download_file(self, remote_file_name: str, progress_callback: Callable = None) -> bool:
        """파일 다운로드"""
        if not self.is_connected:
            self.logger.error("Not connected to SSH server")
            return False
        
        remote_file = self.file_browser.get_remote_file_by_name(remote_file_name)
        if not remote_file:
            self.logger.error(f"Remote file not found: {remote_file_name}")
            return False
        
        if remote_file.is_directory:
            self.logger.error("Directory download not supported yet")
            return False
        
        with self.transfer_lock:
            self.current_transfer = f"Downloading {remote_file_name}"
            success = self.file_browser.download_file(remote_file, progress_callback)
            self.current_transfer = None
        
        return success
    
    def create_remote_directory(self, name: str) -> bool:
        """원격 디렉토리 생성"""
        if not self.is_connected:
            return False
        return self.file_browser.create_remote_directory(name)
    
    def delete_remote_file(self, name: str) -> bool:
        """원격 파일 삭제"""
        if not self.is_connected:
            return False
        
        remote_file = self.file_browser.get_remote_file_by_name(name)
        if not remote_file:
            return False
        
        if remote_file.is_directory:
            return self.file_browser.delete_remote_directory(name)
        else:
            return self.file_browser.delete_remote_file(name)
    
    def refresh_views(self):
        """로컬 및 원격 파일 목록 새로고침"""
        self.file_browser.refresh_local()
        if self.is_connected:
            self.file_browser.refresh_remote()
    
    def get_connection_status(self) -> dict:
        """연결 상태 정보"""
        return {
            'connected': self.is_connected,
            'current_transfer': self.current_transfer,
            'local_path': str(self.file_browser.local_path),
            'remote_path': self.file_browser.remote_path if self.is_connected else None,
            'connection_info': self.ssh_manager.get_connection_info()
        }
    
    def test_connection(self) -> bool:
        """연결 상태 테스트"""
        if not self.is_connected:
            return False
        return self.ssh_manager.is_alive()