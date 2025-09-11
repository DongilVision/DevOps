# SSH 파일 전송 클라이언트

SSH/SFTP를 사용한 파일 전송 클라이언트입니다.

## 기능
- SSH 서버 연결
- 로컬-원격 파일 전송
- 드래그 앤 드롭 지원
- 디렉토리 관리

## 설치
```bash
pip install -r requirements.txt
python run_client.py
```

## 사용법
1. Connect 버튼 클릭
2. SSH 서버 정보 입력
3. 파일 드래그 앤 드롭으로 전송

## 요구사항
- Python 3.8+
- SSH 서버 (Linux, Windows OpenSSH 등)

## 프로젝트 구조
```
FileTransfer/
├── src/client/
│   ├── ssh_connection_manager.py
│   ├── sftp_file_browser.py
│   └── client_ui.py
├── run_client.py
└── requirements.txt
```

## SSH 연결 예시
- 호스트: 192.168.1.100
- 포트: 22
- 사용자: username
- 인증: 패스워드 또는 SSH 키