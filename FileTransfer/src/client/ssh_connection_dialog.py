import os
import json
from pathlib import Path
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, 
    QLabel, QLineEdit, QPushButton, QSpinBox, 
    QMessageBox, QDialogButtonBox, QGroupBox
)
from PySide6.QtCore import Qt
from .dark_theme import DARK_STYLESHEET


class SSHConnectionDialog(QDialog):
    """SSH 연결 설정 다이얼로그 (패스워드 인증만 지원)"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("SSH Connection")
        self.setModal(True)
        self.setFixedSize(350, 250)
        
        # 다크 테마 적용
        self.setStyleSheet(DARK_STYLESHEET)
        
        self.setup_ui()
        self.load_defaults()
    
    def setup_ui(self):
        """UI 구성"""
        layout = QVBoxLayout()
        
        # 서버 정보 그룹
        server_group = QGroupBox("Server Information")
        server_layout = QFormLayout()
        
        # 호스트
        self.host_edit = QLineEdit()
        self.host_edit.setPlaceholderText("192.168.1.100 or server.example.com")
        server_layout.addRow("Host:", self.host_edit)
        
        # 포트
        self.port_spin = QSpinBox()
        self.port_spin.setRange(1, 65535)
        self.port_spin.setValue(22)
        server_layout.addRow("Port:", self.port_spin)
        
        # 사용자명
        self.username_edit = QLineEdit()
        server_layout.addRow("Username:", self.username_edit)
        
        # 패스워드
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        server_layout.addRow("Password:", self.password_edit)
        
        server_group.setLayout(server_layout)
        layout.addWidget(server_group)
        
        # 버튼
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        
        # 테스트 연결 버튼 추가
        self.test_btn = QPushButton("Test Connection")
        self.test_btn.clicked.connect(self.test_connection)
        button_box.addButton(self.test_btn, QDialogButtonBox.ButtonRole.ActionRole)
        
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        layout.addWidget(button_box)
        self.setLayout(layout)
    
    def load_defaults(self):
        """기본값 로드 - host.json에서 자동 로드"""
        try:
            # host.json 파일 경로 찾기
            host_file = None
            
            # 현재 디렉토리에서 찾기
            current_dir = Path.cwd()
            if (current_dir / "host.json").exists():
                host_file = current_dir / "host.json"
            
            # 프로젝트 루트에서 찾기
            project_root = Path(__file__).parent.parent.parent
            if host_file is None and (project_root / "host.json").exists():
                host_file = project_root / "host.json"
            
            if host_file and host_file.exists():
                with open(host_file, 'r', encoding='utf-8') as f:
                    hosts = json.load(f)
                
                if hosts and len(hosts) > 0:
                    host_config = hosts[0]  # 첫 번째 호스트 설정 사용
                    
                    # 필드 자동 채우기
                    self.host_edit.setText(str(host_config.get('host', '')))
                    self.port_spin.setValue(int(host_config.get('port', 22)))
                    self.username_edit.setText(str(host_config.get('username', '')))
                    self.password_edit.setText(str(host_config.get('password', '')))
                    
                    # 상태 표시
                    self.setWindowTitle(f"SSH Connection - Loaded from {host_file.name}")
                    
        except Exception as e:
            # 로드 실패해도 에러를 표시하지 않음 (선택사항이므로)
            print(f"Info: Could not load host.json - {e}")
            pass
    
    def get_connection_info(self) -> tuple:
        """연결 정보 반환 (host, port, username, password)"""
        host = self.host_edit.text().strip()
        port = self.port_spin.value()
        username = self.username_edit.text().strip()
        password = self.password_edit.text()
        
        return host, port, username, password
    
    def validate_input(self) -> bool:
        """입력값 검증"""
        if not self.host_edit.text().strip():
            QMessageBox.warning(self, "Validation Error", "Host is required")
            return False
        
        if not self.username_edit.text().strip():
            QMessageBox.warning(self, "Validation Error", "Username is required")
            return False
        
        if not self.password_edit.text():
            QMessageBox.warning(self, "Validation Error", "Password is required")
            return False
        
        return True
    
    def test_connection(self):
        """연결 테스트"""
        if not self.validate_input():
            return
        
        from .ssh_connection_manager import SSHConnectionManager
        
        # 임시 연결 매니저로 테스트
        test_manager = SSHConnectionManager()
        host, port, username, password = self.get_connection_info()
        
        try:
            success = test_manager.establish_connection(
                host=host,
                port=port,
                username=username,
                password=password
            )
            
            if success:
                QMessageBox.information(self, "Connection Test", "Connection successful!")
                test_manager.close_connection()
            else:
                QMessageBox.warning(self, "Connection Test", "Connection failed!")
                
        except Exception as e:
            QMessageBox.critical(self, "Connection Test", f"Connection error: {str(e)}")
        finally:
            test_manager.close_connection()
    
    def accept(self):
        """다이얼로그 확인"""
        if self.validate_input():
            super().accept()
    
    def get_profile_name(self) -> str:
        """연결 프로파일 이름 생성"""
        host = self.host_edit.text().strip()
        username = self.username_edit.text().strip()
        return f"{username}@{host}"