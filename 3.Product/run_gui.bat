@echo off
echo 8대 장비 ICMP Ping 모니터링 시스템 - GUI 버전
echo ================================================
echo.

REM Python 설치 확인
python --version >nul 2>&1
if errorlevel 1 (
    echo 오류: Python이 설치되어 있지 않습니다.
    echo Python 3.7 이상을 설치해주세요.
    pause
    exit /b 1
)

REM PySide6 설치 확인
python -c "import PySide6" >nul 2>&1
if errorlevel 1 (
    echo PySide6가 설치되어 있지 않습니다. 설치를 시작합니다...
    pip install PySide6>=6.5.0
    if errorlevel 1 (
        echo PySide6 설치에 실패했습니다.
        pause
        exit /b 1
    )
)

echo GUI 모니터링 시스템을 시작합니다...
echo 관리자 권한이 필요할 수 있습니다.
echo.

REM GUI 프로그램 실행
python ping_monitor_gui.py

pause 