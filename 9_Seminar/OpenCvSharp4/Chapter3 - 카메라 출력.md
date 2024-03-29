# 제 3강 - 카메라 출력

## 카메라 출력
내장 카메라 또는 외장 카메라에서 이미지를 불러와 프레임을 재생합니다.
카메라에서 실시간으로 프레임을 읽어 Mat 클래스 형식으로 출력됩니다.

## 메인 코드

```
using System;
using OpenCvSharp;

namespace Project
{
    class Program
    {
        static void Main(string[] args)
        {
            VideoCapture video = new VideoCapture(0);   
            Mat frame = new Mat();                      

            while (Cv2.WaitKey(33) != 'q')
            {
                video.Read(frame);
                Cv2.ImShow("frame", frame);
            }

            frame.Dispose();
            video.Release();
            Cv2.DestroyAllWindows();
        }
    }
}
```
```
VideoCapture video = new VideoCapture(0);   
Mat frame = new Mat();   
```
+ VideoCapture 클래스로 video를 초기화합니다.

+ VideoCapture 클래스는 카메라의 장치 번호를 사용해 카메라와 연결합니다.

+ 클래스의 매개변수의 0은 첫 번째로 연결된 카메라를 의미합니다.

+ 웹캠이 내장된 노트북이나 카메라가 내장돼 있지 않은 컴퓨터에 카메라를 연결하면 장치 번호는 0을 사용합니다.

+ 카메라가 여러 대 연결돼 있다면 0이 아닌 1, 2, 3, … 등의 장치 번호를 사용해 외부 카메라로 전환합니다.

> Tip : 카메라에 대한 접근 권한이 허용돼야 사용이 가능합니다.

+ 이후, 프레임을 표시하기 위해 Mat 클래스인 frame을 초기화합니다.

***

```
while (Cv2.WaitKey(33) != 'q')
{
    ...
}
```
+ 반복문(while)을 활용해, 33ms마다 q키가 입력될 때까지 반복합니다.

+ 키 입력 대기 함수(Cv2.WaitKey)로 특정 시간마다 대기합니다.

+ 키 입력 대기 함수는 Cv2.WaitKey(ms)를 사용해 ms만큼 대기합니다.

+ 또한 반환값을 인식해 활용할 수도 있습니다.

***

```
video.Read(frame);
Cv2.ImShow("frame", frame);
```
+ video의 Read() 메서드를 활용해 프레임을 불러옵니다.

+ video.Read()로 프레임을 읽어 frame 변수에 저장합니다.

+ 이후, 이미지 출력 함수(Cv2.Imshow)로 프레임을 시각적으로 표시합니다.

+ 이미지 출력 함수는 Cv2.Imshow(winname, mat)로 winname의 윈도우 창에 mat 이미지를 표시합니다.
***

```
frame.Dispose();
video.Release();
Cv2.DestroyAllWindows();
```
+ Dispose()와 Release() 구문으로 프레임과 비디오에 대한 메모리를 해제합니다.

+  또한, 윈도우 창을 더 이상 사용하지 않으므로, 모든 윈도우 창을 제거(Cv2.DestroyAllWindows)합니다.

> Tip : 더 이상 사용되지 않는다면, 명시적으로 메모리를 해제해주는 것을 권장합니다.
