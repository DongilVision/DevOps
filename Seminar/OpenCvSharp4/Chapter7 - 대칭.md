# 제 7장 - 대칭

## 대칭

대칭은 기하학적인 측면에서 반사(reflection)의 의미를 갖습니다.

2차원 유클리드 공간에서의 기하학적인 변환의 하나로 
(2차원 유클리드 공간) 위의 선형 변환을 진행합니다.

대칭은 변환할 행렬(이미지)에 대해 2×2 행렬을 왼쪽 곱셈합니다.

## 매칭 코드

```c#
using System;
using OpenCvSharp;

namespace Project
{
    class Program
    {
        static void Main(string[] args)
        {
            Mat src = Cv2.ImRead("bird.jpg");
            Mat dst = new Mat(src.Size(), MatType.CV_8UC3);

            Cv2.Flip(src, dst, FlipMode.Y);

            Cv2.ImShow("dst", dst);
            Cv2.WaitKey(0);
            Cv2.DestroyAllWindows();
        }
    }
}
```

## 세부 코드

```c#
Mat src = Cv2.ImRead("bird.jpg");
Mat dst = new Mat(src.Size(), MatType.CV_8UC3);
```

ImRead 함수를 사용해 이미지를 src에 할당합니다.

dst는 변환된 이미지를 저장할 공간입니다. 데이터는 src와 동일합니다.

색상 공간이 변경되지 않으므로, 원본 이미지의 채널과 동일합니다.

```c#
Cv2.Flip(src, dst, FlipMode.Y);
```

대칭 함수(Cv2.Flip)를 활용해 이미지를 변환합니다.

Cv2.Flip(원본 이미지, 결과 이미지, 대칭 축)로 색상 공간을 변환합니다.

대칭 축(FlipMode)를 사용해 X 축, Y 축, XY 축 대칭을 진행할 수 있습니다.

## 대칭 축 종류 

| 값            | 의미                      |
|---------------|---------------------------|
| FlipMode.X    | X축 대칭 (상하 대칭)      |
| FlipMode.Y    | Y축 대칭 (좌우 대칭)      |
| FlipMode.XY	| XY축 대칭 (상하좌우 대칭) |

## 출력 결과
