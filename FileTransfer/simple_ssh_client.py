#!/usr/bin/env python3
"""
Simple SSH File Transfer Client - CLI Version
host.json을 사용한 간단한 SSH 파일 전송 클라이언트
"""
import sys
import json
import os
from pathlib import Path

# Add the src directory to the Python path
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

def load_host_config():
    """host.json 파일에서 호스트 정보 로드"""
    try:
        host_file = Path(__file__).parent / "host.json"
        with open(host_file, 'r', encoding='utf-8') as f:
            hosts = json.load(f)
        return hosts[0] if hosts else None
    except Exception as e:
        print(f"ERROR: Failed to load host.json - {e}")
        return None

def display_menu():
    """메뉴 표시"""
    print("\n" + "=" * 50)
    print("SSH File Transfer Client")
    print("=" * 50)
    print("1. List remote files")
    print("2. Upload file to server")
    print("3. Download file from server") 
    print("4. Create remote directory")
    print("5. Delete remote file")
    print("6. Connection status")
    print("0. Exit")
    print("=" * 50)

def list_remote_files(ssh_manager):
    """원격 파일 목록 조회"""
    try:
        sftp = ssh_manager.get_sftp_client()
        
        # 현재 디렉토리 확인
        current_dir = sftp.getcwd()
        if current_dir is None:
            current_dir = sftp.normalize('.')
        
        print(f"\nCurrent directory: {current_dir}")
        print("-" * 40)
        
        # 파일 목록 조회
        files = sftp.listdir_attr('.')
        
        if not files:
            print("Directory is empty")
            return
        
        print(f"{'Name':<25} {'Size':<10} {'Type':<10}")
        print("-" * 45)
        
        for file_attr in files:
            name = file_attr.filename
            size = file_attr.st_size if file_attr.st_size else 0
            file_type = "DIR" if file_attr.st_mode and (file_attr.st_mode & 0o170000) == 0o040000 else "FILE"
            
            print(f"{name:<25} {size:<10} {file_type:<10}")
            
        print(f"\nTotal: {len(files)} items")
        
    except Exception as e:
        print(f"ERROR: Failed to list files - {e}")

def upload_file(ssh_manager):
    """파일 업로드"""
    try:
        local_file = input("Local file path: ").strip()
        if not local_file:
            print("ERROR: Local file path required")
            return
        
        local_path = Path(local_file)
        if not local_path.exists():
            print(f"ERROR: Local file not found: {local_file}")
            return
        
        remote_file = input(f"Remote file name (default: {local_path.name}): ").strip()
        if not remote_file:
            remote_file = local_path.name
        
        print(f"Uploading {local_file} -> {remote_file}...")
        
        sftp = ssh_manager.get_sftp_client()
        sftp.put(str(local_path), remote_file)
        
        print("SUCCESS: File uploaded successfully")
        
    except Exception as e:
        print(f"ERROR: Upload failed - {e}")

def download_file(ssh_manager):
    """파일 다운로드"""
    try:
        remote_file = input("Remote file name: ").strip()
        if not remote_file:
            print("ERROR: Remote file name required")
            return
        
        local_file = input(f"Local file path (default: {remote_file}): ").strip()
        if not local_file:
            local_file = remote_file
        
        print(f"Downloading {remote_file} -> {local_file}...")
        
        sftp = ssh_manager.get_sftp_client()
        sftp.get(remote_file, local_file)
        
        print("SUCCESS: File downloaded successfully")
        
    except Exception as e:
        print(f"ERROR: Download failed - {e}")

def create_directory(ssh_manager):
    """원격 디렉토리 생성"""
    try:
        dir_name = input("Directory name: ").strip()
        if not dir_name:
            print("ERROR: Directory name required")
            return
        
        print(f"Creating directory: {dir_name}...")
        
        sftp = ssh_manager.get_sftp_client()
        sftp.mkdir(dir_name)
        
        print("SUCCESS: Directory created successfully")
        
    except Exception as e:
        print(f"ERROR: Directory creation failed - {e}")

def delete_file(ssh_manager):
    """원격 파일 삭제"""
    try:
        file_name = input("File name to delete: ").strip()
        if not file_name:
            print("ERROR: File name required")
            return
        
        confirm = input(f"Delete '{file_name}'? (y/N): ").strip().lower()
        if confirm != 'y':
            print("Deletion cancelled")
            return
        
        print(f"Deleting file: {file_name}...")
        
        sftp = ssh_manager.get_sftp_client()
        sftp.remove(file_name)
        
        print("SUCCESS: File deleted successfully")
        
    except Exception as e:
        print(f"ERROR: File deletion failed - {e}")

def show_connection_status(ssh_manager, host_config):
    """연결 상태 표시"""
    try:
        is_connected = ssh_manager.is_alive()
        
        print("\nConnection Status:")
        print("-" * 30)
        print(f"Server: {host_config['host']}:{host_config['port']}")
        print(f"User: {host_config['username']}")
        print(f"Status: {'CONNECTED' if is_connected else 'DISCONNECTED'}")
        
        if is_connected:
            # 현재 디렉토리 확인
            try:
                sftp = ssh_manager.get_sftp_client()
                current_dir = sftp.getcwd() or sftp.normalize('.')
                print(f"Working Directory: {current_dir}")
            except:
                print("Working Directory: (unable to determine)")
        
    except Exception as e:
        print(f"ERROR: Failed to check connection status - {e}")

def main():
    """메인 함수"""
    print("Simple SSH File Transfer Client")
    print("Loading configuration from host.json...")
    
    # 1. host.json 로드
    host_config = load_host_config()
    if not host_config:
        return 1
    
    print(f"Target: {host_config['username']}@{host_config['host']}:{host_config['port']}")
    
    # 2. SSH 연결 매니저 초기화
    try:
        from client.ssh_connection_manager import SSHConnectionManager
        ssh_manager = SSHConnectionManager()
    except ImportError as e:
        print(f"ERROR: Failed to import SSH manager - {e}")
        return 1
    
    # 3. 연결 시도
    print("Connecting to SSH server...")
    success = ssh_manager.establish_connection(
        host_config['host'],
        host_config['port'], 
        host_config['username'],
        host_config['password']
    )
    
    if not success:
        print("ERROR: Failed to connect to SSH server")
        print("Please check your host.json configuration and server status")
        return 1
    
    print("SUCCESS: Connected to SSH server")
    
    # 4. 메인 루프
    try:
        while True:
            display_menu()
            
            try:
                choice = input("\nSelect option: ").strip()
                
                if choice == '0':
                    break
                elif choice == '1':
                    list_remote_files(ssh_manager)
                elif choice == '2':
                    upload_file(ssh_manager)
                elif choice == '3':
                    download_file(ssh_manager)
                elif choice == '4':
                    create_directory(ssh_manager)
                elif choice == '5':
                    delete_file(ssh_manager)
                elif choice == '6':
                    show_connection_status(ssh_manager, host_config)
                else:
                    print("Invalid option. Please try again.")
                
                input("\nPress Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n\nExiting...")
                break
            except EOFError:
                print("\n\nExiting...")
                break
    
    finally:
        # 5. 연결 종료
        print("\nClosing SSH connection...")
        ssh_manager.close_connection()
        print("Goodbye!")
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)