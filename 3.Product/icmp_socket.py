#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ICMP 소켓 관리 클래스
ICMP 패킷 생성, 전송, 수신 기능을 제공
"""

import socket
import struct
import select
import random
import time
from typing import Dict, Optional


class ICMPSocket:
    """ICMP 소켓 관리 클래스"""
    
    def __init__(self, timeout: float = 1.0):
        self.timeout = timeout
        self.socket = None
        self.identifier = random.randint(1000, 65535)
        # 패킷 통계 추가
        self.tx_count = 0
        self.rx_count = 0
        self.loss_count = 0
    
    def create_socket(self) -> bool:
        """ICMP 소켓 생성"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            self.socket.settimeout(self.timeout)
            return True
        except PermissionError:
            return False
        except Exception:
            return False
    
    def create_icmp_packet(self, sequence: int, data: str = "ping") -> bytes:
        """ICMP Echo Request 패킷 생성"""
        icmp_type = 8  # Echo Request
        icmp_code = 0
        icmp_checksum = 0
        icmp_identifier = self.identifier
        icmp_sequence = sequence
        
        icmp_header = struct.pack('!BBHHH', 
                                 icmp_type, icmp_code, icmp_checksum,
                                 icmp_identifier, icmp_sequence)
        
        data_bytes = data.encode('utf-8')
        if len(data_bytes) < 56:
            data_bytes += b'\x00' * (56 - len(data_bytes))
        
        packet = icmp_header + data_bytes
        checksum = self.calculate_checksum(packet)
        
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
    
    def send_packet(self, packet: bytes, host: str) -> bool:
        """패킷 전송"""
        try:
            self.socket.sendto(packet, (host, 0))
            self.tx_count += 1  # 전송 카운트 증가
            return True
        except Exception:
            return False
    
    def receive_packet(self) -> Optional[tuple]:
        """패킷 수신"""
        try:
            ready = select.select([self.socket], [], [], 0.5)
            if ready[0]:
                packet, addr = self.socket.recvfrom(1024)
                self.rx_count += 1  # 수신 카운트 증가
                return packet, addr
        except Exception:
            pass
        return None
    
    def parse_icmp_response(self, packet: bytes) -> Optional[Dict]:
        """ICMP 응답 패킷 파싱"""
        try:
            icmp_header = packet[20:28]
            icmp_type, icmp_code, checksum, identifier, sequence = struct.unpack('!BBHHH', icmp_header)
            
            if icmp_type == 0:  # Echo Reply
                return {
                    'type': icmp_type,
                    'code': icmp_code,
                    'identifier': identifier,
                    'sequence': sequence,
                    'timestamp': time.time()
                }
        except Exception:
            pass
        
        return None
    
    def get_statistics(self) -> Dict:
        """패킷 통계 반환"""
        total_sent = self.tx_count
        total_received = self.rx_count
        total_lost = self.loss_count
        
        # 손실률 계산
        loss_rate = 0.0
        if total_sent > 0:
            loss_rate = (total_lost / total_sent) * 100
        
        return {
            'tx_count': total_sent,
            'rx_count': total_received,
            'loss_count': total_lost,
            'loss_rate': loss_rate
        }
    
    def reset_statistics(self):
        """통계 초기화"""
        self.tx_count = 0
        self.rx_count = 0
        self.loss_count = 0
    
    def mark_packet_lost(self):
        """패킷 손실 표시"""
        self.loss_count += 1
    
    def close(self):
        """소켓 닫기"""
        if self.socket:
            self.socket.close()
            self.socket = None 