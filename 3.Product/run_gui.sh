#!/bin/bash

echo "8대 장비 ICMP Ping 모니터링 시스템 - GUI 버전"
echo "================================================"
echo

# Python 설치 확인
if ! command -v python3 &> /dev/null; then
    echo "오류: Python3가 설치되어 있지 않습니다."
    echo "Python 3.7 이상을 설치해주세요."
    exit 1
fi

# PySide6 설치 확인
if ! python3 -c "import PySide6" &> /dev/null; then
    echo "PySide6가 설치되어 있지 않습니다. 설치를 시작합니다..."
    pip3 install PySide6>=6.5.0
    if [ $? -ne 0 ]; then
        echo "PySide6 설치에 실패했습니다."
        exit 1
    fi
fi

echo "GUI 모니터링 시스템을 시작합니다..."
echo "관리자 권한이 필요할 수 있습니다."
echo

# GUI 프로그램 실행 (관리자 권한으로)
if [ "$EUID" -ne 0 ]; then
    echo "관리자 권한으로 실행합니다..."
    sudo python3 ping_monitor_gui.py
else
    python3 ping_monitor_gui.py
fi 