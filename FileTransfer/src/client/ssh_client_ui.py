import sys
import logging
from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QSplitter, QToolBar, QStatusBar, QMenuBar, QMessageBox,
    QLabel, QPushButton, QGroupBox, QListWidget, QListWidgetItem,
    QProgressBar, QInputDialog, QDialog
)
from PySide6.QtCore import Qt, QTimer, Signal, QThread
from PySide6.QtGui import QAction, QIcon, QKeySequence

from .ssh_client import SSHFileTransferClient
from .ssh_connection_dialog import SSHConnectionDialog
from .dark_theme import apply_dark_theme


class ConnectionWorker(QThread):
    """SSH 연결 작업 스레드"""
    connection_finished = Signal(bool, str, str)  # success, message, error_detail
    
    def __init__(self, client, host, port, username, password):
        super().__init__()
        self.client = client
        self.host = host
        self.port = port
        self.username = username
        self.password = password
    
    def run(self):
        """연결 실행"""
        try:
            success = self.client.connect(self.host, self.port, self.username, self.password)
            
            if success:
                self.connection_finished.emit(True, f"Successfully connected to {self.host}:{self.port}", "")
            else:
                error_msg = f"Failed to connect to {self.host}:{self.port}"
                detail = "Authentication failed or server unreachable"
                self.connection_finished.emit(False, error_msg, detail)
                
        except Exception as e:
            error_msg = f"Connection error to {self.host}:{self.port}"
            self.connection_finished.emit(False, error_msg, str(e))


class TransferWorker(QThread):
    """파일 전송 작업 스레드"""
    progress_updated = Signal(int)
    transfer_finished = Signal(bool, str)
    
    def __init__(self, client, transfer_type, file_name):
        super().__init__()
        self.client = client
        self.transfer_type = transfer_type  # 'upload' or 'download'
        self.file_name = file_name
        self.progress = 0
    
    def progress_callback(self, transferred, total):
        """전송 진행률 콜백"""
        if total > 0:
            progress = int((transferred / total) * 100)
            self.progress_updated.emit(progress)
    
    def run(self):
        """전송 실행"""
        try:
            if self.transfer_type == 'upload':
                success = self.client.upload_file(self.file_name, self.progress_callback)
            else:
                success = self.client.download_file(self.file_name, self.progress_callback)
            
            message = f"{self.transfer_type.capitalize()} {'successful' if success else 'failed'}"
            self.transfer_finished.emit(success, message)
        except Exception as e:
            self.transfer_finished.emit(False, str(e))


class FileListWidget(QListWidget):
    """파일 목록 위젯"""
    
    def __init__(self, is_remote=False):
        super().__init__()
        self.is_remote = is_remote
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QListWidget.ExtendedSelection)
        self.itemDoubleClicked.connect(self.on_item_double_clicked)
    
    def on_item_double_clicked(self, item):
        """아이템 더블클릭 처리"""
        if item.data(Qt.UserRole) == 'directory':
            # 디렉토리 이동 신호 발생
            self.parent().navigate_to_directory(item.text(), self.is_remote)
    
    def populate_files(self, files):
        """파일 목록 채우기"""
        self.clear()
        
        # 상위 디렉토리 이동 항목 추가
        if hasattr(self.parent(), 'current_path'):
            parent_item = QListWidgetItem("📁 ..")
            parent_item.setData(Qt.UserRole, 'parent')
            self.addItem(parent_item)
        
        # 디렉토리 먼저 추가
        directories = [f for f in files if f.is_directory]
        for directory in directories:
            item_text = f"📁 {directory.name}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, 'directory')
            item.setData(Qt.UserRole + 1, directory.name)
            self.addItem(item)
        
        # 파일 추가
        files_only = [f for f in files if not f.is_directory]
        for file_info in files_only:
            if hasattr(file_info, 'format_size'):
                size_str = file_info.format_size(file_info.size)
            else:
                # SFTPFileInfo의 경우
                from .sftp_file_browser import SFTPFileInfo
                size_str = SFTPFileInfo.format_size(file_info.size)
            
            item_text = f"📄 {file_info.name} ({size_str})"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, 'file')
            item.setData(Qt.UserRole + 1, file_info.name)
            self.addItem(item)


class SSHClientUI(QMainWindow):
    """SSH 파일 전송 클라이언트 메인 UI"""
    
    def __init__(self):
        super().__init__()
        self.client = SSHFileTransferClient()
        self.transfer_worker = None
        self.connection_worker = None
        self.setup_ui()
        self.setup_menu()
        self.setup_toolbar()
        self.setup_status_timer()
    
    def setup_ui(self):
        """UI 구성"""
        self.setWindowTitle("SSH File Transfer Client")
        self.setGeometry(100, 100, 1000, 700)
        
        # 중앙 위젯
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 메인 레이아웃
        main_layout = QVBoxLayout()
        
        # 파일 브라우저 섹션
        browser_splitter = QSplitter(Qt.Horizontal)
        
        # 로컬 파일 그룹
        local_group = QGroupBox("Local Files")
        local_layout = QVBoxLayout()
        
        self.local_path_label = QLabel(str(Path.home()))
        local_layout.addWidget(self.local_path_label)
        
        self.local_list = FileListWidget(is_remote=False)
        local_layout.addWidget(self.local_list)
        
        local_group.setLayout(local_layout)
        browser_splitter.addWidget(local_group)
        
        # 원격 파일 그룹
        remote_group = QGroupBox("Remote Files")
        remote_layout = QVBoxLayout()
        
        self.remote_path_label = QLabel("Not connected")
        remote_layout.addWidget(self.remote_path_label)
        
        self.remote_list = FileListWidget(is_remote=True)
        remote_layout.addWidget(self.remote_list)
        
        remote_group.setLayout(remote_layout)
        browser_splitter.addWidget(remote_group)
        
        browser_splitter.setSizes([500, 500])
        main_layout.addWidget(browser_splitter)
        
        # 전송 컨트롤 섹션
        transfer_group = QGroupBox("Transfer")
        transfer_layout = QHBoxLayout()
        
        self.upload_btn = QPushButton("⬆️ Upload")
        self.upload_btn.setEnabled(False)
        self.upload_btn.clicked.connect(self.upload_selected)
        transfer_layout.addWidget(self.upload_btn)
        
        self.download_btn = QPushButton("⬇️ Download")
        self.download_btn.setEnabled(False)
        self.download_btn.clicked.connect(self.download_selected)
        transfer_layout.addWidget(self.download_btn)
        
        # 진행률 표시
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        transfer_layout.addWidget(self.progress_bar)
        
        # 연결 진행률 표시 (별도)
        self.connection_progress = QProgressBar()
        self.connection_progress.setRange(0, 0)  # 무한 진행률
        self.connection_progress.setVisible(False)
        transfer_layout.addWidget(self.connection_progress)
        
        transfer_group.setLayout(transfer_layout)
        main_layout.addWidget(transfer_group)
        
        central_widget.setLayout(main_layout)
        
        # 상태바
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        # 초기 로컬 파일 로드
        self.refresh_local_files()
    
    def setup_menu(self):
        """메뉴 설정"""
        menubar = self.menuBar()
        
        # File 메뉴
        file_menu = menubar.addMenu("File")
        
        connect_action = QAction("Connect...", self)
        connect_action.setShortcut(QKeySequence("Ctrl+K"))
        connect_action.triggered.connect(self.show_connection_dialog)
        file_menu.addAction(connect_action)
        
        disconnect_action = QAction("Disconnect", self)
        disconnect_action.triggered.connect(self.disconnect)
        file_menu.addAction(disconnect_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence("Ctrl+Q"))
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View 메뉴
        view_menu = menubar.addMenu("View")
        
        refresh_action = QAction("Refresh", self)
        refresh_action.setShortcut(QKeySequence("F5"))
        refresh_action.triggered.connect(self.refresh_all)
        view_menu.addAction(refresh_action)
    
    def setup_toolbar(self):
        """툴바 설정"""
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)
        
        # Connect 버튼
        self.connect_action = QAction("🔗 Connect", self)
        self.connect_action.triggered.connect(self.show_connection_dialog)
        toolbar.addAction(self.connect_action)
        
        # Disconnect 버튼
        self.disconnect_action = QAction("❌ Disconnect", self)
        self.disconnect_action.triggered.connect(self.disconnect)
        self.disconnect_action.setEnabled(False)
        toolbar.addAction(self.disconnect_action)
        
        toolbar.addSeparator()
        
        # Refresh 버튼
        refresh_action = QAction("🔄 Refresh", self)
        refresh_action.triggered.connect(self.refresh_all)
        toolbar.addAction(refresh_action)
        
        toolbar.addSeparator()
        
        # New Folder 버튼
        self.mkdir_action = QAction("📁 New Folder", self)
        self.mkdir_action.triggered.connect(self.create_remote_directory)
        self.mkdir_action.setEnabled(False)
        toolbar.addAction(self.mkdir_action)
        
        # Delete 버튼
        self.delete_action = QAction("🗑️ Delete", self)
        self.delete_action.triggered.connect(self.delete_remote_file)
        self.delete_action.setEnabled(False)
        toolbar.addAction(self.delete_action)
    
    def setup_status_timer(self):
        """상태 업데이트 타이머"""
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_status)
        self.status_timer.start(5000)  # 5초마다 업데이트
    
    def show_connection_dialog(self):
        """연결 다이얼로그 표시"""
        dialog = SSHConnectionDialog(self)
        if dialog.exec() == QDialog.Accepted:
            host, port, username, password = dialog.get_connection_info()
            self.connect_to_server(host, port, username, password)
    
    def connect_to_server(self, host, port, username, password):
        """서버 연결 (비동기)"""
        if self.connection_worker and self.connection_worker.isRunning():
            QMessageBox.warning(self, "Connection in Progress", 
                              "Another connection attempt is already in progress")
            return
        
        # 연결 시작 UI 업데이트
        self.status_bar.showMessage("Connecting...")
        self.connection_progress.setVisible(True)
        self.connect_action.setEnabled(False)
        
        # 비동기 연결 시작
        self.connection_worker = ConnectionWorker(self.client, host, port, username, password)
        self.connection_worker.connection_finished.connect(self.on_connection_finished)
        self.connection_worker.start()
    
    def on_connection_finished(self, success, message, error_detail):
        """연결 완료 처리"""
        # UI 상태 복원
        self.connection_progress.setVisible(False)
        self.connect_action.setEnabled(True)
        
        if success:
            self.status_bar.showMessage(message)
            self.remote_path_label.setText(self.client.file_browser.remote_path)
            self.refresh_remote_files()
            
            # UI 상태 업데이트
            self.connect_action.setEnabled(False)
            self.disconnect_action.setEnabled(True)
            self.upload_btn.setEnabled(True)
            self.download_btn.setEnabled(True)
            self.mkdir_action.setEnabled(True)
            self.delete_action.setEnabled(True)
            
            QMessageBox.information(self, "Connection Successful", message)
        else:
            # 연결 실패 시 상세 메시지
            if error_detail:
                error_msg = f"{message}\n\nError details:\n{error_detail}\n\n" \
                           f"Please check:\n" \
                           f"• Network connectivity\n" \
                           f"• Server credentials\n" \
                           f"• SSH server configuration\n" \
                           f"• Firewall settings"
            else:
                error_msg = f"{message}\n\nPossible reasons:\n" \
                           f"• Server is not running or unreachable\n" \
                           f"• Incorrect hostname or port\n" \
                           f"• Invalid username or password\n" \
                           f"• Firewall blocking connection\n" \
                           f"• SSH service not enabled on server"
            
            QMessageBox.critical(self, "Connection Failed", error_msg)
            self.status_bar.showMessage("Connection failed")
    
    def disconnect(self):
        """서버 연결 해제"""
        self.client.disconnect()
        self.status_bar.showMessage("Disconnected")
        self.remote_path_label.setText("Not connected")
        self.remote_list.clear()
        
        # UI 상태 업데이트
        self.connect_action.setEnabled(True)
        self.disconnect_action.setEnabled(False)
        self.upload_btn.setEnabled(False)
        self.download_btn.setEnabled(False)
        self.mkdir_action.setEnabled(False)
        self.delete_action.setEnabled(False)
    
    def refresh_local_files(self):
        """로컬 파일 새로고침"""
        self.client.file_browser.refresh_local()
        files = self.client.get_local_files()
        self.local_list.populate_files(files)
        self.local_path_label.setText(str(self.client.file_browser.local_path))
    
    def refresh_remote_files(self):
        """원격 파일 새로고침"""
        if self.client.is_connected:
            self.client.file_browser.refresh_remote()
            files = self.client.get_remote_files()
            self.remote_list.populate_files(files)
            self.remote_path_label.setText(self.client.file_browser.remote_path)
    
    def refresh_all(self):
        """모든 파일 목록 새로고침"""
        self.refresh_local_files()
        self.refresh_remote_files()
    
    def navigate_to_directory(self, dir_name, is_remote):
        """디렉토리 이동"""
        if dir_name == "..":
            if is_remote:
                self.client.file_browser.navigate_up_remote()
            else:
                self.client.file_browser.navigate_up_local()
        else:
            if is_remote:
                import os
                new_path = os.path.join(self.client.file_browser.remote_path, dir_name)
                self.client.navigate_remote(new_path)
            else:
                new_path = self.client.file_browser.local_path / dir_name
                self.client.navigate_local(new_path)
        
        # 파일 목록 새로고침
        if is_remote:
            self.refresh_remote_files()
        else:
            self.refresh_local_files()
    
    def upload_selected(self):
        """선택된 파일 업로드"""
        selected_items = self.local_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select files to upload")
            return
        
        for item in selected_items:
            if item.data(Qt.UserRole) == 'file':
                file_name = item.data(Qt.UserRole + 1)
                self.start_transfer('upload', file_name)
                break  # 현재는 한 번에 하나씩만
    
    def download_selected(self):
        """선택된 파일 다운로드"""
        selected_items = self.remote_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select files to download")
            return
        
        for item in selected_items:
            if item.data(Qt.UserRole) == 'file':
                file_name = item.data(Qt.UserRole + 1)
                self.start_transfer('download', file_name)
                break  # 현재는 한 번에 하나씩만
    
    def start_transfer(self, transfer_type, file_name):
        """파일 전송 시작"""
        if self.transfer_worker and self.transfer_worker.isRunning():
            QMessageBox.warning(self, "Transfer in Progress", 
                              "Another transfer is already in progress")
            return
        
        self.transfer_worker = TransferWorker(self.client, transfer_type, file_name)
        self.transfer_worker.progress_updated.connect(self.update_progress)
        self.transfer_worker.transfer_finished.connect(self.transfer_finished)
        
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)
        self.status_bar.showMessage(f"{transfer_type.capitalize()}ing {file_name}...")
        
        self.transfer_worker.start()
    
    def update_progress(self, progress):
        """진행률 업데이트"""
        self.progress_bar.setValue(progress)
    
    def transfer_finished(self, success, message):
        """전송 완료 처리"""
        self.progress_bar.setVisible(False)
        self.status_bar.showMessage(message)
        
        if success:
            # 파일 목록 새로고침
            self.refresh_all()
        else:
            QMessageBox.warning(self, "Transfer Failed", message)
    
    def create_remote_directory(self):
        """원격 디렉토리 생성"""
        if not self.client.is_connected:
            return
        
        name, ok = QInputDialog.getText(self, "Create Directory", "Directory name:")
        if ok and name.strip():
            if self.client.create_remote_directory(name.strip()):
                self.refresh_remote_files()
            else:
                QMessageBox.warning(self, "Error", "Failed to create directory")
    
    def delete_remote_file(self):
        """원격 파일 삭제"""
        selected_items = self.remote_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select files to delete")
            return
        
        for item in selected_items:
            if item.data(Qt.UserRole) in ['file', 'directory']:
                file_name = item.data(Qt.UserRole + 1)
                reply = QMessageBox.question(self, "Confirm Delete", 
                                           f"Delete {file_name}?")
                if reply == QMessageBox.Yes:
                    if self.client.delete_remote_file(file_name):
                        self.refresh_remote_files()
                    else:
                        QMessageBox.warning(self, "Error", f"Failed to delete {file_name}")
                break
    
    def update_status(self):
        """주기적 상태 업데이트"""
        if self.client.is_connected:
            if not self.client.test_connection():
                self.disconnect()
                QMessageBox.warning(self, "Connection Lost", 
                                  "SSH connection has been lost")


def main():
    app = QApplication(sys.argv)
    
    # 다크 테마 적용
    apply_dark_theme(app)
    
    # 로깅 설정
    logging.basicConfig(level=logging.INFO)
    
    window = SSHClientUI()
    window.show()
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())