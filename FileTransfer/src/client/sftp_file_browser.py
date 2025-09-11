"""
SFTP 파일 브라우저 모듈
"""
import logging
import stat
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Callable

from .ssh_connection_manager import SSHConnectionManager
from src.common.file_info import FileInfo


class SFTPFileInfo:
    """SFTP 파일 정보 클래스"""
    
    def __init__(self, name: str, attributes):
        self.name = name
        self.size = attributes.st_size
        self.is_directory = stat.S_ISDIR(attributes.st_mode)
        self.modified_time = datetime.fromtimestamp(attributes.st_mtime)
        self.attributes = attributes
    
    @staticmethod
    def format_size(size_bytes: int) -> str:
        """바이트를 읽기 쉬운 형태로 변환"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        size = float(size_bytes)
        
        while size >= 1024.0 and i < len(size_names) - 1:
            size /= 1024.0
            i += 1
        
        return f"{size:.1f} {size_names[i]}"
    
    def __repr__(self):
        return f"SFTPFileInfo(name='{self.name}', size={self.size}, is_dir={self.is_directory})"


class SFTPFileBrowser:
    """SFTP 파일 브라우저 클래스"""
    
    def __init__(self, ssh_manager: SSHConnectionManager):
        self.ssh_manager = ssh_manager
        self.local_path = Path.home()
        self.remote_path = "/"
        self.local_files: List[FileInfo] = []
        self.remote_files: List[SFTPFileInfo] = []
        self.logger = logging.getLogger(__name__)
    
    def refresh_local(self):
        """로컬 파일 목록 새로고침"""
        try:
            self.local_files = []
            if self.local_path.exists() and self.local_path.is_dir():
                for item in self.local_path.iterdir():
                    try:
                        file_info = FileInfo(item)
                        self.local_files.append(file_info)
                    except (OSError, IOError) as e:
                        self.logger.warning(f"Could not access local file {item}: {e}")
            
            # 디렉토리 먼저, 그 다음 파일 순으로 정렬
            self.local_files.sort(key=lambda x: (not x.is_directory, x.name.lower()))
            
        except Exception as e:
            self.logger.error(f"Error refreshing local files: {e}")
            self.local_files = []
    
    def refresh_remote(self):
        """원격 파일 목록 새로고침"""
        try:
            self.remote_files = []
            sftp_client = self.ssh_manager.get_sftp_client()
            
            for item in sftp_client.listdir_attr(self.remote_path):
                try:
                    file_info = SFTPFileInfo(item.filename, item)
                    self.remote_files.append(file_info)
                except Exception as e:
                    self.logger.warning(f"Could not access remote file {item.filename}: {e}")
            
            # 디렉토리 먼저, 그 다음 파일 순으로 정렬
            self.remote_files.sort(key=lambda x: (not x.is_directory, x.name.lower()))
            
        except Exception as e:
            self.logger.error(f"Error refreshing remote files: {e}")
            self.remote_files = []
    
    def navigate_to_local(self, path: Path):
        """로컬 디렉토리 이동"""
        if path.exists() and path.is_dir():
            self.local_path = path
            self.refresh_local()
        else:
            self.logger.error(f"Local path does not exist or is not a directory: {path}")
    
    def navigate_to_remote(self, path: str):
        """원격 디렉토리 이동"""
        try:
            sftp_client = self.ssh_manager.get_sftp_client()
            # 경로 존재 여부 확인
            sftp_client.stat(path)
            self.remote_path = path
            self.refresh_remote()
        except Exception as e:
            self.logger.error(f"Remote path does not exist or is not accessible: {path} - {e}")
    
    def navigate_up_local(self):
        """로컬 상위 디렉토리로 이동"""
        if self.local_path.parent != self.local_path:
            self.navigate_to_local(self.local_path.parent)
    
    def navigate_up_remote(self):
        """원격 상위 디렉토리로 이동"""
        if self.remote_path != "/":
            parent_path = "/".join(self.remote_path.rstrip("/").split("/")[:-1])
            if not parent_path:
                parent_path = "/"
            self.navigate_to_remote(parent_path)
    
    def get_local_file_by_name(self, name: str) -> Optional[FileInfo]:
        """이름으로 로컬 파일 찾기"""
        for file_info in self.local_files:
            if file_info.name == name:
                return file_info
        return None
    
    def get_remote_file_by_name(self, name: str) -> Optional[SFTPFileInfo]:
        """이름으로 원격 파일 찾기"""
        for file_info in self.remote_files:
            if file_info.name == name:
                return file_info
        return None
    
    def upload_file(self, local_file: FileInfo, progress_callback: Callable = None) -> bool:
        """파일 업로드"""
        try:
            sftp_client = self.ssh_manager.get_sftp_client()
            remote_file_path = f"{self.remote_path.rstrip('/')}/{local_file.name}"
            
            # 진행률 콜백이 있는 경우
            if progress_callback:
                def callback(transferred, total):
                    progress_callback(transferred, total)
                
                sftp_client.put(str(local_file.path), remote_file_path, callback=callback)
            else:
                sftp_client.put(str(local_file.path), remote_file_path)
            
            self.logger.info(f"Successfully uploaded {local_file.name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Upload failed for {local_file.name}: {e}")
            return False
    
    def download_file(self, remote_file: SFTPFileInfo, progress_callback: Callable = None) -> bool:
        """파일 다운로드"""
        try:
            sftp_client = self.ssh_manager.get_sftp_client()
            remote_file_path = f"{self.remote_path.rstrip('/')}/{remote_file.name}"
            local_file_path = self.local_path / remote_file.name
            
            # 진행률 콜백이 있는 경우
            if progress_callback:
                def callback(transferred, total):
                    progress_callback(transferred, total)
                
                sftp_client.get(remote_file_path, str(local_file_path), callback=callback)
            else:
                sftp_client.get(remote_file_path, str(local_file_path))
            
            self.logger.info(f"Successfully downloaded {remote_file.name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Download failed for {remote_file.name}: {e}")
            return False
    
    def create_remote_directory(self, name: str) -> bool:
        """원격 디렉토리 생성"""
        try:
            sftp_client = self.ssh_manager.get_sftp_client()
            remote_dir_path = f"{self.remote_path.rstrip('/')}/{name}"
            sftp_client.mkdir(remote_dir_path)
            
            self.logger.info(f"Successfully created remote directory {name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to create remote directory {name}: {e}")
            return False
    
    def delete_remote_file(self, name: str) -> bool:
        """원격 파일 삭제"""
        try:
            sftp_client = self.ssh_manager.get_sftp_client()
            remote_file_path = f"{self.remote_path.rstrip('/')}/{name}"
            sftp_client.remove(remote_file_path)
            
            self.logger.info(f"Successfully deleted remote file {name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to delete remote file {name}: {e}")
            return False
    
    def delete_remote_directory(self, name: str) -> bool:
        """원격 디렉토리 삭제"""
        try:
            sftp_client = self.ssh_manager.get_sftp_client()
            remote_dir_path = f"{self.remote_path.rstrip('/')}/{name}"
            sftp_client.rmdir(remote_dir_path)
            
            self.logger.info(f"Successfully deleted remote directory {name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to delete remote directory {name}: {e}")
            return False
