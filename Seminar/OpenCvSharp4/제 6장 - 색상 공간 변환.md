# 제 6장 - 색상 공간 변환

## 색상 공간 변환

색상 공간 변환은 본래의 색상 공간에서 다른 색상 공간으로 변환할 때 사용합니다.

색상 공간 변환 함수는 데이터 타입을 같게 유지하고 채널을 변환합니다.

## 메인 코드

```c#
using System;
using OpenCvSharp;

namespace Project
{
    class Program
    {
        static void Main(string[] args)
        {
            Mat src = Cv2.ImRead("desert.jpg");
            Mat dst = new Mat(src.Size(), MatType.CV_8UC1);

            Cv2.CvtColor(src, dst, ColorConversionCodes.BGR2GRAY);

            Cv2.ImShow("dst", dst);
            Cv2.WaitKey(0);
            Cv2.DestroyAllWindows();
        }
    }
}
```

## 세부 코드

```c#
Mat src = Cv2.ImRead("desert.jpg");             // ImRead 함수를 사용해 이미지를 src에 할당
Mat dst = new Mat(src.Size(), MatType.CV_8UC1); // dst는 변환된 이미지를 저장할 공간
```

ImRead 함수를 사용해 이미지를 src에 할당합니다.

dst는 변환된 이미지를 저장할 공간입니다. 채널의 값을 1로 사용합니다.

>Tip : 3채널 이미지에서 1채널 이미지로 변환할 예정이므로, 단일 채널을 사용합니다.

```c#
Cv2.CvtColor(src, dst, ColorConversionCodes.BGR2GRAY); 
```

색상 공간 변환함수(Cv2.CvtColor)를 활용해 이미지를 변환합니다.

Cv2.CvtColor(원본 이미지, 결과 이미지, 색상 변환 코드)로 색상 공간을 변환합니다.

색상 변환 코드(code)를 사용해 BGR 색상 공간을 RGBA 색상 공간으로 변환하거나 그레이스케일, HSV, CIE Luv 등으로 변환이 가능합니다.

> + BGR2GRAY: BGR 색상 공간에서 흑백(그레이스케일)로 변환합니다. 출력 이미지는 단일 채널로 표시됩니다.
>
> + BGR2HSV: BGR 색상 공간에서 HSV 색상 공간으로 변환합니다.
>
> + BGR2RGB: BGR 색상 공간에서 RGB 색상 공간으로 변환합니다.
>
> + HSV2BGR: HSV 색상 공간에서 BGR 색상 공간으로 변환합니다.
>
> + RGB2BGR: RGB 색상 공간에서 BGR 색상 공간으로 변환합니다.
>
> + GRAY2BGR: 흑백(그레이스케일) 이미지를 BGR 이미지로 변환합니다. 출력 이미지는 3개의 채널을 가지며, 단일 채널의 값으로 복사됩니다.
>
> + HSV2RGB: HSV 색상 공간에서 RGB 색상 공간으로 변환합니다.
>
> + RGB2HSV: RGB 색상 공간에서 HSV 색상 공간으로 변환합니다.

단일 채널부터 3채널, 4채널의 색상 공간으로도 변환이 가능합니다.

단, 그레이스케일(GRAY) 변환은 다중 채널에서 단일 채너로 변환하기 때문에 dst의 채널 수는 1이어야 합니다.

## 출력 결과