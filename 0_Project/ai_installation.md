# < AI Installation >

## 0. 목차
1. 윈도우 설치
2. IMI Neptune 설치
3. CuDa 설치
4. cuDNN 설치
5. TensorRT 설치
6. < 참고 >

## 1. 윈도우 설치 (소요시간 : 20~30분)
- 윈도우 설치용 USB 컴퓨터에 삽입. 
- 바이오스 진입 
- 부팅순서 변경(윈도우 설치 usb로 변경)
- 기본설정으로 계속 진행
- 제품키가없음 클릭
- 사용자 지정 : Windows만 설치(고급) 클릭
- 포멧후 윈도우 설치(사용하지 않는 드라이브 전부 삭제하여 드라이브 1개로 만들기)
- 기본설정으로 계속 진행(한국어, 자판설정 등)
- 계정추가 -> 아무 아이디 입력(ex. ID : a, PW : a) -> 오류 발생으로 계정 입력하지 않고 윈도우 설치가 가능해집니다.
- PC 이름 설정 : DIV
- 비밀번호 : (없음) (다음을 클릭하여 그냥 넘어갑니다.)
- 위치허용 아니요, 내 장치 찾기 아니오, 진단 데이터 보내기 필수 진단 데이터 보내기, 수동 입력 및 타이핑 개선 아니요, 진단 데이터를 사용한 맞춤형 환경 사용아니요, 앱 광고아니오, 사용자 환경을 사용자 지정하세요건너뛰기
- 윈도우 설치 완료


<br>

## 2. IMI Neptune 설치
- 다운로드
    1. google에 IMI tech검색 (http://www.imi-tech.com/home/)
    2. 고객지원 -> 자료실 -> VISION의 모델명 Neptune X 86_x_64 다운로드
- 설치

<br>

## 3. CUDA 설치 (소요시간 : 10분, 다운로드 시간 별도)
- CUDA 다운로드 (방법1)
    1. google에 CUDA검색
    2. Nvidia Tookit - Free Tools and Training - NVIDIA Developer 접속 (https://developer.nvidia.com/cuda-toolkit)
    3. 상단 메뉴에서 Download -> CUDA Toolkit -> DOWNLOAD 
    4. 그래픽카드 버전과 윈도우 버전에 맞는 것으로 다운 (Installer Type = exe(local))
        + RTX 30 시리즈 : 11.X
        + RTX 40 시리즈 : 12.X
- CUDA 다운로드 (방법2) - 하단 참조
- 그래픽카드 드라이버 설치 
    1. nvidia 드라이버 접속합니다.
    2. 그래픽 카드에 맞는 드라이버를 다운로드 및 설치합니다.
    3. 작업관리자에 들어가서 그래픽카드가 정상적으로 인식이 되는지 확인합니다.
- CUDA 설치 
    1. cuda_11.7.1_516.94_windows실행하여 CUDA 설치 
    2. 기본 설적으로 계속 진행(시스템 검사, 라이선스 계약(동의), 옵션) 
- 설치완료

<br>

## 4. cuDNN 설치 (소요시간 : 20분, 다운로드 시간 별도)
- 다운로드(방법1)
    1. google에 cuDNN 검색 CUDA Deep Neural Network (cuDNN) - NVIDIA Developer클릭 (https://developer.nvidia.com/cudnn)
    2. Download cuDNN 클릭
    3. 체크박스에 체크 I Agree To the Terms of the cuDNN Software License Agreement
    4. Download cuDNN v8.9.3 (July 11th, 2023), for CUDA 11.x를 클릭
        + RTX 30 시리즈 : 11.x
        + RTX 40 시리즈 : 12.x
    5. Local Installers for Windows and Linux, Ubuntu(x86_64, armsbsa)의 Local Installer for Windows (Zip)를 다운로드. 
- 다운로드(방법2) - 하단 참조
- 설치
    1. zip파일을 압축을 해제합니다.
    2. cuda가 있는 파일로 이동하여 zip파일 안에 있는 파일들을 전부 복사 붙여넣기 하여 덮어쓰기 합니다.

- 테스트 (여기까지 설치가 완료되면 제대로 작동이 되는지 테스트합니다.)
    0. Anaconda와 vsCode를 설치합니다. (직접 찾아서 설치하거나 글 하단을 참고합니다.)
    1. https://github.com/ultralytics/ultralytics 주소로 이동합니다.
    2. <>Code 클릭하여 Dowload ZIP을 클릭하여 저장하고 압축을 해제하고 vsCode로 파일을 엽니다. 
    3. vsCode 좌측 extension(확장) 클릭. python 검색. python과 python extension pack을 설치합니다.
    4. vsCode에 상단 메뉴에서 터미널 -> 새 터미널 클릭하면 하단에 터미널이 보이는데, 그 터미널에서 우측 상단에 아랫 방향 화살표클릭 Command Prompt를 클릭합니다. (파이썬 코드는 Command Prompt를 사용합니다.)
    5. Command Prompt에 python 을 입력하여 제대로 설치 되었는지 확인하고 exit()로 다시 나갑니다.
    6. https://pytorch.org/get-started/previous-versions/ 에 접속 -> CUDA버전에 맞는 곳을 찾기 (ex. Cuda 11.7) -> pip라고 써져있는 곳을 전부 복사(복사시 세번클릭 말고 드래그를 사용, 맨 끝에 다른 문자가 추가되면 안됨) -> Command Prompt에 붙여넣기후 실행 -> 설치 완료
    7. 라이브러리 다운 : pip3 install -r requirements.txt을 터미널에 입력 -> 설치 완료
    8. https://docs.ultralytics.com/modes/predict/#plotting-results 이동 -> <streaming_for_loop> 코드를 복사 -> vsCode에 test.py파일을 생성하고 복사한 코드를 입력 -> 코드에서 cvs.videocapture(0)으로 수정
    9. 카메라 연결후 실행하면 자동으로 카메라 관련 파일들을 다운로드후 카메라가 실행됩니다. 
    10. 카메라를 이리저리 돌려보면서 사물 인식이 제대로 되는지 확인합니다. 
    11. 작업관리자를 열어서 gpu 사용률이 올라가는지 확인합니다. 
    12. Ctrl + c를 눌러 카메라를 종료합니다.

<br>

## 5. TensorRT 설치 (소요시간 : 20분, 다운로드 시간 별도) => 수정 필요(진행에 문제가 되는 부분이 생길시 김수현님에게 다시 물어보기)
- 다운로드
    1. google에 tensorRT 검색 TensorRT SDK - NVIDIA Developer클릭 (https://developer.nvidia.com/tensorrt)
    2. Get Started -> Download Now -> TensorRT 8(최신버전을 클릭)
    3. 체크박스 체크
    4. TensorRT 8.6 GA (최신버전을 클릭)
    5. 다운로드한 CUDA버전이 있는지 확인하고 Window용으로 ZIP파일을 다운로드 합니다.
- 설치
    1. TensorRT-8.4.3.1.Windows10.x86_64.cuda-11.6.cudnn8.4을 압축해제하여 cuda가 설치 되어있는 파일 옆에 저장한다. 
    2. 환경변수 설정 : TensorRT-8.4.3.1.Windows10.x86_64.cuda-11.6.cudnn8.4안의 lib파일의 경로를 복사 -> 컴퓨터에서  시스템 환경 변수 편집 검색후 실행 -> 환경변수 - 시스템변수 - 변수 - Path을 찾아서 더블클릭한다. -> 환경 변수 편집 - 새로 만들기 클릭 -> 복사한 경로를 붙여넣기 후 재부팅한다(환경 변수 설정을 하여도 적용이 안되는 경우가 있기에 재부팅을 한다.)
    3. https://docs.ultralytics.com/modes/predict/#plotting-results 로 이동. 
    4. 좌측의 메뉴바에서 Export 클릭
    5. 스크롤을 조금만 내리면 Usage Examples가 보입니다. 거기서 CLI 클릭후 첫줄을 복사합니다. (ex. yolo export model=yolov8n.pt format=onnx) (주석문까지 복사하지 않도록 주의)
    6. command Prompt에 붙여넣기 하고 실행하면 설치를 자동으로 진행합니다. 
    7. yolo export model=yolov8n.pt device=0 format=engine 실행
    8. 엄청나게 많은 글씨들이 위로 올라가면 설치가 정상적으로 되고 있다는 신호입니다.
    9.  설치 완료. 


---
## < 참고 >
다운로드 하고자 하는 파일은 서버에 저장되어 있습니다. 
다운로드 속도가 느리거나 급할때 사용합니다.
버전에 맞는 것을 다운받아야 하기 때문에 잘 확인하고 사용합니다.

- 192.168.2.52 접속 -> ID : samba, PW : 1234 -> hdd_0으로 이동 -> installation 이동
- Anaconda3-2023.03-Windows-x86_64, cuda_11.7.1_516.94_windows, cudnn-windows-x86_64-8.8.1.3_cuda11-archive, TensorRT-8.4.3.1.Windows10.x86_64.cuda-11.6.cudnn8.4, VSCodeUserSetup-x64-1.76.2 을 이용합니다. 