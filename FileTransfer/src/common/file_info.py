"""
파일 정보 클래스들
"""
import os
from datetime import datetime
from pathlib import Path
from typing import Optional


class FileInfo:
    """로컬 파일 정보 클래스"""
    
    def __init__(self, path: Path):
        self.path = path
        self.name = path.name
        self.is_directory = path.is_dir()
        self.size = self._get_size()
        self.modified_time = self._get_modified_time()
    
    def _get_size(self) -> int:
        """파일 크기 조회"""
        if self.is_directory:
            return 0
        try:
            return self.path.stat().st_size
        except (OSError, IOError):
            return 0
    
    def _get_modified_time(self) -> Optional[datetime]:
        """수정 시간 조회"""
        try:
            timestamp = self.path.stat().st_mtime
            return datetime.fromtimestamp(timestamp)
        except (OSError, IOError):
            return None
    
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
        return f"FileInfo(name='{self.name}', size={self.size}, is_dir={self.is_directory})"
