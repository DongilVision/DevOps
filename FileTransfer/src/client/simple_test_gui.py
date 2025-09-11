#!/usr/bin/env python3
"""
간단한 SSH 접속 시험용 GUI
"""
import sys
import logging
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QPushButton, QTextEdit, 
    QSpinBox, QProgressBar, QMessageBox
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont

from .ssh_connection_manager import SSHConnectionManager
from .dark_theme import apply_dark_theme


class TestConnectionWorker(QThread):
    """테스트 연결 작업 스레드"""
    test_finished = Signal(bool, str)
    
    def __init__(self, host, port, username, password):
        super().__init__()
        self.host = host
        self.port = port
        self.username = username
        self.password = password
    
    def run(self):
        """연결 테스트 실행"""
        ssh_manager = SSHConnectionManager()
        
        try:
            import socket
            
            # 1단계: TCP 연결 테스트
            self.test_finished.emit(False, f"🔍 1단계: TCP 연결 테스트 중... ({self.host}:{self.port})")
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                result = sock.connect_ex((self.host, self.port))
                sock.close()
                
                if result != 0:
                    error_msg = f"❌ TCP 연결 실패\n"
                    error_msg += f"호스트 {self.host}:{self.port}에 연결할 수 없습니다.\n"
                    error_msg += f"• 서버가 실행 중인지 확인하세요\n"
                    error_msg += f"• 방화벽 설정을 확인하세요\n"
                    error_msg += f"• 포트 번호가 올바른지 확인하세요"
                    self.test_finished.emit(False, error_msg)
                    return
                    
            except Exception as tcp_error:
                error_msg = f"❌ TCP 연결 테스트 실패: {str(tcp_error)}"
                self.test_finished.emit(False, error_msg)
                return
            
            # 2단계: SSH 연결 테스트
            self.test_finished.emit(False, "🔍 2단계: SSH 연결 시도 중...")
            success = ssh_manager.establish_connection(
                self.host, self.port, self.username, self.password
            )
            
            if success:
                # 3단계: SFTP 테스트
                self.test_finished.emit(False, "🔍 3단계: SFTP 기능 테스트 중...")
                try:
                    sftp_client = ssh_manager.get_sftp_client()
                    files = sftp_client.listdir('.')
                    current_dir = sftp_client.getcwd() or sftp_client.normalize('.')
                    
                    message = f"✅ 모든 테스트 통과!\n\n"
                    message += f"🔗 TCP 연결: OK\n"
                    message += f"🔐 SSH 인증: OK\n"
                    message += f"📁 SFTP 접속: OK\n\n"
                    message += f"서버: {self.host}:{self.port}\n"
                    message += f"사용자: {self.username}\n"
                    message += f"현재 디렉토리: {current_dir}\n"
                    message += f"파일/폴더 수: {len(files)}개"
                    
                    # 처음 몇 개 파일/폴더 표시
                    if files:
                        message += f"\n\n📋 디렉토리 내용 (최대 5개):\n"
                        for i, file in enumerate(files[:5]):
                            message += f"  • {file}\n"
                        if len(files) > 5:
                            message += f"  ... 및 {len(files) - 5}개 더"
                    
                    ssh_manager.close_connection()
                    self.test_finished.emit(True, message)
                    
                except Exception as sftp_error:
                    error_msg = f"❌ SFTP 테스트 실패\n"
                    error_msg += f"SSH 연결은 성공했지만 SFTP 접속에 실패했습니다.\n"
                    error_msg += f"오류: {str(sftp_error)}"
                    self.test_finished.emit(False, error_msg)
            else:
                error_msg = f"❌ SSH 연결 실패\n"
                error_msg += f"TCP 연결은 성공했지만 SSH 인증에 실패했습니다.\n"
                error_msg += f"• 사용자명과 비밀번호를 확인하세요\n"
                error_msg += f"• SSH 서비스가 활성화되어 있는지 확인하세요"
                self.test_finished.emit(False, error_msg)
                
        except Exception as e:
            error_msg = f"❌ 테스트 중 예외 발생: {str(e)}"
            import traceback
            error_msg += f"\n\n🔧 디버그 정보:\n{traceback.format_exc()}"
            self.test_finished.emit(False, error_msg)
        finally:
            if ssh_manager:
                ssh_manager.close_connection()


class SimpleTestGUI(QWidget):
    """간단한 SSH 접속 테스트 GUI"""
    
    def __init__(self):
        super().__init__()
        self.test_worker = None
        self.setup_ui()
        
    def setup_ui(self):
        """UI 구성"""
        self.setWindowTitle("SSH 접속 테스트")
        self.setFixedSize(500, 400)
        
        layout = QVBoxLayout()
        
        # 제목
        title = QLabel("SSH/SFTP 접속 테스트")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # 연결 정보 입력
        form_layout = QVBoxLayout()
        
        # 호스트
        host_layout = QHBoxLayout()
        host_layout.addWidget(QLabel("호스트:"))
        self.host_input = QLineEdit()
        self.host_input.setPlaceholderText("예: 192.168.1.100")
        host_layout.addWidget(self.host_input)
        form_layout.addLayout(host_layout)
        
        # 포트
        port_layout = QHBoxLayout()
        port_layout.addWidget(QLabel("포트:"))
        self.port_input = QSpinBox()
        self.port_input.setRange(1, 65535)
        self.port_input.setValue(22)
        port_layout.addWidget(self.port_input)
        port_layout.addStretch()
        form_layout.addLayout(port_layout)
        
        # 사용자명
        user_layout = QHBoxLayout()
        user_layout.addWidget(QLabel("사용자:"))
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("SSH 사용자명")
        user_layout.addWidget(self.username_input)
        form_layout.addLayout(user_layout)
        
        # 비밀번호
        pass_layout = QHBoxLayout()
        pass_layout.addWidget(QLabel("비밀번호:"))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("SSH 비밀번호")
        pass_layout.addWidget(self.password_input)
        form_layout.addLayout(pass_layout)
        
        layout.addLayout(form_layout)
        
        # 테스트 버튼
        button_layout = QHBoxLayout()
        self.test_button = QPushButton("🔍 연결 테스트")
        self.test_button.setMinimumHeight(40)
        self.test_button.clicked.connect(self.test_connection)
        button_layout.addWidget(self.test_button)
        
        self.clear_button = QPushButton("🗑️ 지우기")
        self.clear_button.setMinimumHeight(40)
        self.clear_button.clicked.connect(self.clear_form)
        button_layout.addWidget(self.clear_button)
        
        layout.addLayout(button_layout)
        
        # 진행률 표시
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # 결과 표시
        self.result_text = QTextEdit()
        self.result_text.setMaximumHeight(120)
        self.result_text.setPlaceholderText("테스트 결과가 여기에 표시됩니다...")
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_text)
        
        # 하단 정보
        info_label = QLabel("💡 SSH 서버에 연결하여 SFTP 작동을 확인합니다")
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setStyleSheet("color: #888888; font-size: 10px;")
        layout.addWidget(info_label)
        
        self.setLayout(layout)
        
        # Enter 키로 테스트 실행
        self.password_input.returnPressed.connect(self.test_connection)
    
    def test_connection(self):
        """연결 테스트 시작"""
        # 입력 검증
        host = self.host_input.text().strip()
        port = self.port_input.value()
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not host:
            QMessageBox.warning(self, "입력 오류", "호스트를 입력하세요")
            self.host_input.setFocus()
            return
            
        if not username:
            QMessageBox.warning(self, "입력 오류", "사용자명을 입력하세요")
            self.username_input.setFocus()
            return
            
        if not password:
            QMessageBox.warning(self, "입력 오류", "비밀번호를 입력하세요")
            self.password_input.setFocus()
            return
        
        # 이미 테스트 중인지 확인
        if self.test_worker and self.test_worker.isRunning():
            QMessageBox.information(self, "테스트 진행중", "이미 테스트가 진행 중입니다")
            return
        
        # UI 상태 변경
        self.test_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.result_text.clear()
        self.result_text.append("🔄 연결 테스트 중...")
        
        # 테스트 시작
        self.test_worker = TestConnectionWorker(host, port, username, password)
        self.test_worker.test_finished.connect(self.on_test_finished)
        self.test_worker.start()
    
    def on_test_finished(self, success, message):
        """테스트 완료 처리"""
        # UI 상태 복원
        self.test_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        # 결과 표시
        self.result_text.clear()
        self.result_text.append(message)
        
        if success:
            self.result_text.setStyleSheet("color: #00ff00;")
        else:
            self.result_text.setStyleSheet("color: #ff6666;")
    
    def clear_form(self):
        """폼 지우기"""
        self.host_input.clear()
        self.port_input.setValue(22)
        self.username_input.clear()
        self.password_input.clear()
        self.result_text.clear()
        self.result_text.setStyleSheet("")
        self.host_input.setFocus()


def main():
    """메인 함수"""
    app = QApplication(sys.argv)
    
    # 다크 테마 적용
    apply_dark_theme(app)
    
    # 로깅 설정 (디버깅을 위해 상세하게)
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # GUI 실행
    window = SimpleTestGUI()
    window.show()
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())