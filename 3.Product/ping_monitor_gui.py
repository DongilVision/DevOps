#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
8대 장비 ICMP Ping 모니터링 시스템 - GUI 버전
PySide6를 사용한 사용자 친화적인 인터페이스
"""

import sys
import threading
import time
import socket
import struct
import select
import random
from datetime import datetime
from typing import Dict, List, Optional
import queue

from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QGridLayout, QLabel, QPushButton, 
                               QLineEdit, QTextEdit, QTableWidget, QTableWidgetItem,
                               QHeaderView, QGroupBox, QSpinBox, QProgressBar,
                               QMessageBox, QSplitter, QFrame, QCheckBox)
from PySide6.QtCore import QThread, QTimer, Signal, Qt
from PySide6.QtGui import QFont, QColor, QPalette

from icmp_socket import ICMPSocket


class PingWorker(QThread):
    """Ping 모니터링 워커 스레드"""
    status_updated = Signal(dict)  # 상태 업데이트 시그널
    log_updated = Signal(str)      # 로그 업데이트 시그널
    
    def __init__(self, target_hosts: List[str], timeout: float = 1.0):
        super().__init__()
        self.target_hosts = target_hosts
        self.timeout = timeout
        self.running = False
        
        # ICMP 소켓
        self.icmp_socket = ICMPSocket(timeout)
        
        # 결과 저장용 딕셔너리
        self.results = {}
        self.lock = threading.Lock()
        
        # 각 호스트별 카운터
        self.host_counters = {}
        for host in target_hosts:
            self.host_counters[host] = {
                'sent': 0,
                'received': 0
            }
        
        # 통계
        self.stats = {
            'total_sent': 0,
            'total_received': 0,
            'total_lost': 0
        }
    
    def run(self):
        """메인 실행 루프"""
        if not self.icmp_socket.create_socket():
            self.log_updated.emit("오류: ICMP 소켓 생성에 관리자 권한이 필요합니다.")
            return
        
        self.running = True
        sequence = 0
        
        while self.running:
            for host in self.target_hosts:
                if not self.running:
                    break
                
                try:
                    # ICMP 패킷 생성 및 전송
                    packet = self.icmp_socket.create_icmp_packet(sequence, f"ping_{host}")
                    if self.icmp_socket.send_packet(packet, host):
                        # 전송 정보 저장
                        with self.lock:
                            if host not in self.results:
                                self.results[host] = []
                            
                            self.results[host].append({
                                'sequence': sequence,
                                'sent_time': time.time(),
                                'status': 'sent'
                            })
                            
                            self.host_counters[host]['sent'] += 1
                            self.stats['total_sent'] += 1
                        
                        self.log_updated.emit(f"[{datetime.now().strftime('%H:%M:%S')}] {host}로 패킷 전송 (seq={sequence})")
                        
                        sequence += 1
                        
                        # 응답 수신 대기
                        response_data = self.icmp_socket.receive_packet()
                        if response_data:
                            packet, addr = response_data
                            response = self.icmp_socket.parse_icmp_response(packet)
                            
                            if response:
                                host = addr[0]
                                sequence = response['sequence']
                                receive_time = response['timestamp']
                                
                                with self.lock:
                                    if host in self.results:
                                        for result in self.results[host]:
                                            if result.get('sequence') == sequence and result.get('status') == 'sent':
                                                result['status'] = 'received'
                                                result['receive_time'] = receive_time
                                                result['rtt'] = (receive_time - result['sent_time']) * 1000
                                                
                                                self.host_counters[host]['received'] += 1
                                                self.stats['total_received'] += 1
                                                break
                                
                                self.log_updated.emit(f"[{datetime.now().strftime('%H:%M:%S')}] {host}에서 응답 수신 (seq={sequence}, RTT={result['rtt']:.2f}ms)")
                    
                    # 상태 업데이트 시그널 발생
                    self.update_status()
                    
                    time.sleep(1)
                    
                except Exception as e:
                    self.log_updated.emit(f"패킷 전송 오류 ({host}): {e}")
                    time.sleep(1)
        
        self.icmp_socket.close()
    
    def update_status(self):
        """상태 업데이트 시그널 발생"""
        status_data = {}
        
        with self.lock:
            for host in self.target_hosts:
                if host in self.host_counters:
                    sent_count = self.host_counters[host]['sent']
                    received_count = self.host_counters[host]['received']
                    
                    # RTT 계산을 위해 최근 결과 확인
                    if host in self.results:
                        recent_results = self.results[host][-10:]
                        received_results = [r for r in recent_results if r.get('status') == 'received']
                        
                        if received_results:
                            avg_rtt = sum([r.get('rtt', 0) for r in received_results]) / len(received_results)
                            status = "ONLINE"
                            rtt = avg_rtt
                        else:
                            status = "OFFLINE"
                            rtt = 0
                    else:
                        status = "대기중"
                        rtt = 0
                    
                    status_data[host] = {
                        'status': status,
                        'rtt': rtt,
                        'sent': sent_count,
                        'received': received_count
                    }
                else:
                    status_data[host] = {
                        'status': '대기중',
                        'rtt': 0,
                        'sent': 0,
                        'received': 0
                    }
            
            status_data['stats'] = self.stats.copy()
        
        self.status_updated.emit(status_data)
    
    def stop(self):
        """모니터링 중지"""
        self.running = False


class PingMonitorGUI(QMainWindow):
    """Ping 모니터링 GUI 메인 윈도우"""
    
    def __init__(self):
        super().__init__()
        self.ping_worker = None
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_status_display)
        
        self.init_ui()
        self.init_default_hosts()
    
    def init_ui(self):
        """UI 초기화"""
        self.setWindowTitle("4대 장비 ICMP Ping 모니터링 시스템")
        self.setGeometry(100, 100, 1200, 800)
        
        # 중앙 위젯
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 메인 레이아웃
        main_layout = QVBoxLayout(central_widget)
        
        # 제목
        title_label = QLabel("4대 장비 ICMP Ping 모니터링 시스템")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # 설정 그룹
        config_group = QGroupBox("장비 설정")
        config_layout = QVBoxLayout(config_group)
        
        # 장비 설정 테이블
        self.config_table = QTableWidget()
        self.config_table.setColumnCount(8)
        self.config_table.setRowCount(4)
        self.config_table.setHorizontalHeaderLabels(["장비명", "IP 주소", "활성화", "상태", "RTT (ms)", "송신", "수신", "손실"])
        
        # 테이블 헤더 설정
        header = self.config_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(7, QHeaderView.ResizeToContents)
        
        # 기본 장비명 설정
        for i in range(4):
            self.config_table.setItem(i, 0, QTableWidgetItem(f"장비 {i+1}"))
            # 초기 상태 설정
            self.config_table.setItem(i, 3, QTableWidgetItem("대기중"))
            self.config_table.setItem(i, 4, QTableWidgetItem("0"))
            self.config_table.setItem(i, 5, QTableWidgetItem("0"))
            self.config_table.setItem(i, 6, QTableWidgetItem("0"))
            self.config_table.setItem(i, 7, QTableWidgetItem("0"))
        
        config_layout.addWidget(self.config_table)
        
        # 타임아웃 설정
        timeout_layout = QHBoxLayout()
        timeout_label = QLabel("타임아웃 (초):")
        self.timeout_spin = QSpinBox()
        self.timeout_spin.setRange(1, 10)
        self.timeout_spin.setValue(1)
        
        timeout_layout.addWidget(timeout_label)
        timeout_layout.addWidget(self.timeout_spin)
        timeout_layout.addStretch()
        
        config_layout.addLayout(timeout_layout)
        main_layout.addWidget(config_group)
        
        # 제어 버튼
        control_layout = QHBoxLayout()
        
        self.start_button = QPushButton("모니터링 시작")
        self.start_button.clicked.connect(self.start_monitoring)
        self.start_button.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; padding: 10px; font-size: 14px; }")
        
        self.stop_button = QPushButton("모니터링 중지")
        self.stop_button.clicked.connect(self.stop_monitoring)
        self.stop_button.setEnabled(False)
        self.stop_button.setStyleSheet("QPushButton { background-color: #f44336; color: white; padding: 10px; font-size: 14px; }")
        
        self.clear_button = QPushButton("로그 지우기")
        self.clear_button.clicked.connect(self.clear_log)
        self.clear_button.setStyleSheet("QPushButton { background-color: #2196F3; color: white; padding: 10px; font-size: 14px; }")
        
        control_layout.addWidget(self.start_button)
        control_layout.addWidget(self.stop_button)
        control_layout.addWidget(self.clear_button)
        control_layout.addStretch()
        
        main_layout.addLayout(control_layout)
        
        # 통계 및 로그 분할
        splitter = QSplitter(Qt.Vertical)
        
        # 통계 그룹
        stats_group = QGroupBox("전체 통계")
        stats_layout = QVBoxLayout(stats_group)
        
        self.stats_label = QLabel("통계 정보가 여기에 표시됩니다.")
        self.stats_label.setFont(QFont("Arial", 10))
        stats_layout.addWidget(self.stats_label)
        
        splitter.addWidget(stats_group)
        
        # 로그 그룹
        log_group = QGroupBox("실시간 로그")
        log_layout = QVBoxLayout(log_group)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setFont(QFont("Consolas", 9))
        log_layout.addWidget(self.log_text)
        
        splitter.addWidget(log_group)
        
        main_layout.addWidget(splitter)
        
        # 상태 표시줄
        self.statusBar().showMessage("준비됨")
    
    def init_default_hosts(self):
        """기본 IP 주소 설정"""
        default_hosts = [
            "172.30.1.66",  # 장비 1
            "192.168.1.100", # 장비 2
            "192.168.1.101", # 장비 3
            "192.168.1.102"  # 장비 4
        ]
        
        for i, host in enumerate(default_hosts):
            if i < 4:
                # IP 주소 입력 필드 설정
                ip_input = QLineEdit()
                ip_input.setText(host)
                ip_input.setPlaceholderText("예: 192.168.1.100")
                self.config_table.setCellWidget(i, 1, ip_input)
                
                # 활성화 체크박스 설정 (기본적으로 모두 활성화)
                checkbox = QCheckBox()
                checkbox.setChecked(True)
                self.config_table.setCellWidget(i, 2, checkbox)
    
    def get_target_hosts(self):
        """활성화된 장비의 IP 주소 목록 가져오기"""
        hosts = []
        for row in range(4):
            # IP 주소 가져오기 (LineEdit 위젯에서)
            ip_widget = self.config_table.cellWidget(row, 1)
            if ip_widget:
                ip = ip_widget.text().strip()
                
                # 활성화 상태 확인 (2번 컬럼)
                checkbox = self.config_table.cellWidget(row, 2)
                if checkbox and checkbox.isChecked() and ip:
                    hosts.append(ip)
        
        return hosts
    
    def start_monitoring(self):
        """모니터링 시작"""
        hosts = self.get_target_hosts()
        
        if not hosts:
            QMessageBox.warning(self, "경고", "최소 하나의 활성화된 장비가 필요합니다.")
            return
        
        # 중복 IP 확인
        if len(hosts) != len(set(hosts)):
            QMessageBox.warning(self, "경고", "중복된 IP 주소가 있습니다.")
            return
        
        try:
            # Ping 워커 시작
            self.ping_worker = PingWorker(hosts, self.timeout_spin.value())
            self.ping_worker.status_updated.connect(self.on_status_updated)
            self.ping_worker.log_updated.connect(self.on_log_updated)
            self.ping_worker.start()
            
            # UI 상태 변경
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            
            # 설정 테이블의 상태 컬럼 초기화
            for row in range(4):
                ip_widget = self.config_table.cellWidget(row, 1)
                checkbox = self.config_table.cellWidget(row, 2)
                
                if ip_widget and checkbox and checkbox.isChecked():
                    # 활성화된 장비만 상태 초기화
                    self.config_table.setItem(row, 3, QTableWidgetItem("대기중"))
                    self.config_table.setItem(row, 4, QTableWidgetItem("0"))
                    self.config_table.setItem(row, 5, QTableWidgetItem("0"))
                    self.config_table.setItem(row, 6, QTableWidgetItem("0"))
                    self.config_table.setItem(row, 7, QTableWidgetItem("0"))
                else:
                    # 비활성화된 장비는 상태를 비활성화로 표시
                    self.config_table.setItem(row, 3, QTableWidgetItem("비활성화"))
                    self.config_table.setItem(row, 4, QTableWidgetItem("-"))
                    self.config_table.setItem(row, 5, QTableWidgetItem("-"))
                    self.config_table.setItem(row, 6, QTableWidgetItem("-"))
                    self.config_table.setItem(row, 7, QTableWidgetItem("-"))
            
            # 상태 업데이트 타이머 시작
            self.status_timer.start(1000)  # 1초마다 업데이트
            
            self.statusBar().showMessage("모니터링 중...")
            self.log_text.append(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 모니터링 시작됨")
            
        except Exception as e:
            QMessageBox.critical(self, "오류", f"모니터링 시작 실패: {e}")
    
    def stop_monitoring(self):
        """모니터링 중지"""
        if self.ping_worker:
            self.ping_worker.stop()
            self.ping_worker.wait()
            self.ping_worker = None
        
        # UI 상태 변경
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        
        # 상태 업데이트 타이머 중지
        self.status_timer.stop()
        
        self.statusBar().showMessage("모니터링 중지됨")
        self.log_text.append(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 모니터링 중지됨")
    
    def on_status_updated(self, status_data):
        """상태 업데이트 처리"""
        self.current_status = status_data
    
    def update_status_display(self):
        """상태 표시 업데이트"""
        if not hasattr(self, 'current_status'):
            return
        
        # 테이블 업데이트
        for row in range(4):
            # IP 주소 가져오기 (LineEdit 위젯에서)
            ip_widget = self.config_table.cellWidget(row, 1)
            if ip_widget:
                host = ip_widget.text().strip()
                if host in self.current_status:
                    status_info = self.current_status[host]
                    
                    # 상태
                    status_item = QTableWidgetItem(status_info['status'])
                    if status_info['status'] == 'ONLINE':
                        status_item.setBackground(QColor(200, 255, 200))  # 연한 녹색
                    elif status_info['status'] == 'OFFLINE':
                        status_item.setBackground(QColor(255, 200, 200))  # 연한 빨간색
                    else:
                        status_item.setBackground(QColor(255, 255, 200))  # 연한 노란색
                    
                    self.config_table.setItem(row, 3, status_item)
                    
                    # RTT
                    rtt_item = QTableWidgetItem(f"{status_info['rtt']:.2f}")
                    self.config_table.setItem(row, 4, rtt_item)
                    
                    # 송신
                    sent_item = QTableWidgetItem(str(status_info['sent']))
                    self.config_table.setItem(row, 5, sent_item)
                    
                    # 수신
                    received_item = QTableWidgetItem(str(status_info['received']))
                    self.config_table.setItem(row, 6, received_item)
                    
                    # 손실 (송신 - 수신)
                    lost = status_info['sent'] - status_info['received']
                    lost_item = QTableWidgetItem(str(lost))
                    self.config_table.setItem(row, 7, lost_item)
        
        # 전체 통계 업데이트
        if 'stats' in self.current_status:
            stats = self.current_status['stats']
            total_sent = stats.get('total_sent', 0)
            total_received = stats.get('total_received', 0)
            total_lost = total_sent - total_received
            
            if total_sent > 0:
                loss_rate = (total_lost / total_sent) * 100
                stats_text = f"전체 송신: {total_sent}, 수신: {total_received}, 손실: {total_lost} (손실률: {loss_rate:.2f}%)"
            else:
                stats_text = "통계 정보 없음"
            
            self.stats_label.setText(stats_text)
    
    def on_log_updated(self, message):
        """로그 업데이트 처리"""
        self.log_text.append(message)
        # 자동 스크롤
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def clear_log(self):
        """로그 지우기"""
        self.log_text.clear()
    
    def closeEvent(self, event):
        """윈도우 종료 이벤트"""
        if self.ping_worker and self.ping_worker.isRunning():
            reply = QMessageBox.question(self, "확인", 
                                       "모니터링이 실행 중입니다. 정말 종료하시겠습니까?",
                                       QMessageBox.Yes | QMessageBox.No)
            
            if reply == QMessageBox.Yes:
                self.stop_monitoring()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


def main():
    """메인 함수"""
    app = QApplication(sys.argv)
    
    # 애플리케이션 스타일 설정
    app.setStyle('Fusion')
    
    # 다크 테마 (선택사항)
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
    palette.setColor(QPalette.Text, QColor(255, 255, 255))
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
    palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    app.setPalette(palette)
    
    window = PingMonitorGUI()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main() 