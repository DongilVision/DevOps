# 제 5장 - Video 출력

## 동영상 출력

컴퓨터에 저장된 동영상 파일에서 이미지를 불러와 프레임을 재생합니다.

동영상 파일에 저장된 프레임을 읽어 Mat 클래스 형식으로 출력됩니다.



## 메인 코드

``` c#
using System;
using OpenCvSharp;

namespace Project
{
    class Program
    {
        static void Main(string[] args)
        {
            VideoCapture video = new VideoCapture("ocean.mp4");
            Mat frame = new Mat();

            while (video.PosFrames != video.FrameCount)
            {
                video.Read(frame);
                Cv2.ImShow("frame", frame);
                Cv2.WaitKey(33);
            }

            frame.Dispose();
            video.Release();
            Cv2.DestroyAllWindows();
        }
    }
}
```

## 세부 코드
```c#
VideoCapture video = new VideoCapture("ocean.mp4"); // VideoCapture 클래스 video 초기화
Mat frame = new Mat();                              // Mat 클래스 frame 초기화
```
VideoCapture 클래스로 video를 초기화합니다.

VideoCapture 클래스는 동영상 파일 저장경로를 입력해 동영상을 불러옵니다.

경로는 상대 경로 또는 절대 경로를 사용해 이미지를 지정합니다.

이후, 프레임을 표시하기 위해 Mat 클래스인 frame을 초기화합니다.
```c#
while (video.PosFrames != video.FrameCount) // 반복해서 프레임 불러오기

{
    ...
}
```
반복문(while)을 활용해 현재 프레임이 동영상 파일의 총 프레임과 같아질 때까지 반복합니다.

video의 속성 중 현재 프레임을 불러오는 PosFrames과 총 프레임을 불러오는 FrameCount를 사용합니다.

PosFrames은 현재 프레임의 개수를 나타내며, FrameCount는 총 프레임의 개수를 나타냅니다.

```c#
video.Read(frame);          // video의 Read() 메서드를 활용해 프레임을 불러 frame 변수에 저장
Cv2.ImShow("frame", frame); // 이미지 출력 함수(Cv2.Imshow)로 프레임을 시각적으로 표시
Cv2.WaitKey(33);            // 33ms. 영상의 속도를 조절.
```
video의 Read() 메서드를 활용해 프레임을 불러옵니다.

video.Read()로 프레임을 읽어 frame 변수에 저장합니다.

이후, 이미지 출력 함수(Cv2.Imshow)로 프레임을 시각적으로 표시합니다.

이미지 출력 함수는 Cv2.Imshow(winname, mat)로 winname의 윈도우 창에 mat 이미지를 표시합니다.

마지막으로 키 입력 대기 함수(Cv2.WaitKey)로 특정 시간마다 대기합니다.

키 입력 대기 함수는 Cv2.WaitKey(ms)를 사용해 ms만큼 대기합니다.

```c#
frame.Dispose();            // frame 메모리 해제
video.Release();            // video 메모리 해제
Cv2.DestroyAllWindows();    // 윈도우 창을 제거 
```
Dispose()와 Release() 구문으로 프레임과 비디오에 대한 메모리를 해제합니다.

또한, 윈도우 창을 더 이상 사용하지 않으므로, 모든 윈도우 창을 제거(Cv2.DestroyAllWindows)합니다.

>Tip : 더 이상 사용되지 않는다면, 명시적으로 메모리를 해제해주는 것을 권장합니다.

## 출력 결과
