#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
8대 장비 ICMP Ping 모니터링 시스템
- 순차적으로 ping 패킷 전송
- 하나의 수신 스레드로 모든 응답 감시
- 실시간 상태 모니터링
"""

import threading
import time
import socket
import struct
import select
import random
import sys
from datetime import datetime
from typing import Dict, List, Optional
import queue

class ICMPPingMonitor:
    def __init__(self, target_hosts: List[str], timeout: float = 1.0):
        """
        ICMP Ping 모니터 초기화
        
        Args:
            target_hosts: 모니터링할 호스트 목록
            timeout: ping 타임아웃 (초)
        """
        self.target_hosts = target_hosts
        self.timeout = timeout
        self.running = False
        
        # 결과 저장용 딕셔너리
        self.results = {}
        self.lock = threading.Lock()
        
        # 응답 수신용 큐
        self.response_queue = queue.Queue()
        
        # ICMP 소켓
        self.icmp_socket = None
        
        # 스레드들
        self.sender_thread = None
        self.receiver_thread = None
        
        # 통계
        self.stats = {
            'total_sent': 0,
            'total_received': 0,
            'total_lost': 0
        }
    
    def create_icmp_socket(self):
        """ICMP 소켓 생성"""
        try:
            # ICMP 프로토콜 소켓 생성
            self.icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            self.icmp_socket.settimeout(self.timeout)
            return True
        except PermissionError:
            print("오류: ICMP 소켓 생성에 관리자 권한이 필요합니다.")
            print("Windows에서는 관리자 권한으로 실행하거나, Linux에서는 sudo로 실행하세요.")
            return False
        except Exception as e:
            print(f"소켓 생성 오류: {e}")
            return False
    
    def create_icmp_packet(self, identifier: int, sequence: int, data: str = "ping") -> bytes:
        """
        ICMP Echo Request 패킷 생성
        
        Args:
            identifier: 패킷 식별자
            sequence: 시퀀스 번호
            data: 패킷 데이터
            
        Returns:
            ICMP 패킷 바이트
        """
        # ICMP 헤더 (8바이트)
        icmp_type = 8  # Echo Request
        icmp_code = 0
        icmp_checksum = 0
        icmp_identifier = identifier
        icmp_sequence = sequence
        
        # ICMP 헤더 생성
        icmp_header = struct.pack('!BBHHH', 
                                 icmp_type, icmp_code, icmp_checksum,
                                 icmp_identifier, icmp_sequence)
        
        # 데이터 생성 (최소 56바이트)
        data_bytes = data.encode('utf-8')
        if len(data_bytes) < 56:
            data_bytes += b'\x00' * (56 - len(data_bytes))
        
        # 체크섬 계산
        packet = icmp_header + data_bytes
        checksum = self.calculate_checksum(packet)
        
        # 체크섬을 포함한 최종 패킷
        icmp_header = struct.pack('!BBHHH',
                                 icmp_type, icmp_code, checksum,
                                 icmp_identifier, icmp_sequence)
        
        return icmp_header + data_bytes
    
    def calculate_checksum(self, data: bytes) -> int:
        """ICMP 체크섬 계산"""
        if len(data) % 2 == 1:
            data += b'\x00'
        
        sum_val = 0
        for i in range(0, len(data), 2):
            sum_val += (data[i] << 8) + data[i + 1]
        
        sum_val = (sum_val >> 16) + (sum_val & 0xffff)
        sum_val += sum_val >> 16
        
        return (~sum_val) & 0xffff
    
    def parse_icmp_response(self, packet: bytes) -> Optional[Dict]:
        """
        ICMP 응답 패킷 파싱
        
        Args:
            packet: 수신된 패킷
            
        Returns:
            파싱된 응답 정보 또는 None
        """
        try:
            # IP 헤더 (20바이트) 건너뛰기
            icmp_header = packet[20:28]
            icmp_type, icmp_code, checksum, identifier, sequence = struct.unpack('!BBHHH', icmp_header)
            
            # Echo Reply인지 확인
            if icmp_type == 0:  # Echo Reply
                return {
                    'type': icmp_type,
                    'code': icmp_code,
                    'identifier': identifier,
                    'sequence': sequence,
                    'timestamp': time.time()
                }
        except Exception as e:
            print(f"패킷 파싱 오류: {e}")
        
        return None
    
    def sender_worker(self):
        """송신 스레드 워커"""
        print("송신 스레드 시작")
        
        sequence = 0
        identifier = random.randint(1000, 65535)
        
        while self.running:
            for host in self.target_hosts:
                if not self.running:
                    break
                
                try:
                    # ICMP 패킷 생성
                    packet = self.create_icmp_packet(identifier, sequence, f"ping_{host}")
                    
                    # 패킷 전송
                    self.icmp_socket.sendto(packet, (host, 0))
                    
                    # 전송 정보 저장
                    with self.lock:
                        if host not in self.results:
                            self.results[host] = []
                        
                        self.results[host].append({
                            'sequence': sequence,
                            'sent_time': time.time(),
                            'status': 'sent'
                        })
                        
                        self.stats['total_sent'] += 1
                    
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] {host}로 패킷 전송 (seq={sequence})")
                    
                    sequence += 1
                    
                    # 1초 대기
                    time.sleep(1)
                    
                except Exception as e:
                    print(f"패킷 전송 오류 ({host}): {e}")
                    time.sleep(1)
        
        print("송신 스레드 종료")
    
    def receiver_worker(self):
        """수신 스레드 워커"""
        print("수신 스레드 시작")
        
        while self.running:
            try:
                # 소켓에서 데이터 수신 대기
                ready = select.select([self.icmp_socket], [], [], 0.1)
                
                if ready[0]:
                    packet, addr = self.icmp_socket.recvfrom(1024)
                    
                    # ICMP 응답 파싱
                    response = self.parse_icmp_response(packet)
                    
                    if response:
                        host = addr[0]
                        sequence = response['sequence']
                        receive_time = response['timestamp']
                        
                        # 결과 업데이트
                        with self.lock:
                            if host in self.results:
                                # 해당 시퀀스의 패킷 찾기
                                for result in self.results[host]:
                                    if result.get('sequence') == sequence and result.get('status') == 'sent':
                                        result['status'] = 'received'
                                        result['receive_time'] = receive_time
                                        result['rtt'] = (receive_time - result['sent_time']) * 1000  # ms
                                        
                                        self.stats['total_received'] += 1
                                        break
                        
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] {host}에서 응답 수신 (seq={sequence}, RTT={result['rtt']:.2f}ms)")
                
            except socket.timeout:
                continue
            except Exception as e:
                print(f"수신 오류: {e}")
                continue
        
        print("수신 스레드 종료")
    
    def monitor_worker(self):
        """모니터링 스레드 워커"""
        print("모니터링 스레드 시작")
        
        while self.running:
            try:
                # 현재 상태 출력
                self.print_status()
                
                # 5초마다 상태 출력
                time.sleep(5)
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"모니터링 오류: {e}")
        
        print("모니터링 스레드 종료")
    
    def print_status(self):
        """현재 상태 출력"""
        print("\n" + "="*60)
        print(f"Ping 모니터링 상태 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        with self.lock:
            for host in self.target_hosts:
                if host in self.results:
                    recent_results = self.results[host][-10:]  # 최근 10개 결과
                    
                    sent_count = len([r for r in recent_results if r.get('status') == 'sent'])
                    received_count = len([r for r in recent_results if r.get('status') == 'received'])
                    
                    if received_count > 0:
                        avg_rtt = sum([r.get('rtt', 0) for r in recent_results if r.get('status') == 'received']) / received_count
                        status = f"ONLINE (RTT: {avg_rtt:.2f}ms)"
                    else:
                        status = "OFFLINE"
                    
                    print(f"{host:15} | {status:20} | 송신: {sent_count}, 수신: {received_count}")
                else:
                    print(f"{host:15} | {'대기중':20} | 송신: 0, 수신: 0")
        
        # 전체 통계
        print("-"*60)
        print(f"전체 통계 | 송신: {self.stats['total_sent']}, 수신: {self.stats['total_received']}")
        if self.stats['total_sent'] > 0:
            loss_rate = ((self.stats['total_sent'] - self.stats['total_received']) / self.stats['total_sent']) * 100
            print(f"패킷 손실률: {loss_rate:.2f}%")
        print("="*60)
    
    def start(self):
        """모니터링 시작"""
        if not self.create_icmp_socket():
            return False
        
        self.running = True
        
        # 스레드 시작
        self.sender_thread = threading.Thread(target=self.sender_worker, daemon=True)
        self.receiver_thread = threading.Thread(target=self.receiver_worker, daemon=True)
        self.monitor_thread = threading.Thread(target=self.monitor_worker, daemon=True)
        
        self.sender_thread.start()
        self.receiver_thread.start()
        self.monitor_thread.start()
        
        print("Ping 모니터링 시작됨")
        print("종료하려면 Ctrl+C를 누르세요")
        
        try:
            # 메인 스레드에서 대기
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n모니터링 종료 중...")
            self.stop()
        
        return True
    
    def stop(self):
        """모니터링 중지"""
        self.running = False
        
        if self.icmp_socket:
            self.icmp_socket.close()
        
        # 스레드 종료 대기
        if self.sender_thread:
            self.sender_thread.join(timeout=2)
        if self.receiver_thread:
            self.receiver_thread.join(timeout=2)
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2)
        
        print("모니터링이 종료되었습니다.")


def main():
    """메인 함수"""
    # 모니터링할 8대 장비 IP 주소
    target_hosts = [
        "172.30.1.66",  # 장비 1
    ]
    
    print("8대 장비 ICMP Ping 모니터링 시스템")
    print("="*50)
    print("모니터링 대상:")
    for i, host in enumerate(target_hosts, 1):
        print(f"  장비 {i}: {host}")
    print("="*50)
    
    # 실제 사용할 IP 주소 입력 받기
    print("\n실제 모니터링할 IP 주소를 입력하세요 (엔터로 기본값 사용):")
    custom_hosts = []
    
    for i, default_host in enumerate(target_hosts, 1):
        user_input = input(f"장비 {i} IP (기본: {default_host}): ").strip()
        if user_input:
            custom_hosts.append(user_input)
        else:
            custom_hosts.append(default_host)
    
    # 모니터링 시작
    monitor = ICMPPingMonitor(custom_hosts, timeout=1.0)
    monitor.start()


if __name__ == "__main__":
    main()
