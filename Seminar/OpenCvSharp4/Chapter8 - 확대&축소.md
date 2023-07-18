# 제 8강 - 확대 & 축소

## 확대 & 축소

확대와 축소는 입력 이미지의 크기를 단계적으로 변화시켜 원하는 단계에 도달할 때까지 진행하는 이미지 피라미드를 사용합니다.

객체가 너무 작거나 입력 이미지가 너무 큰 경우 입력 이미지 자체를 변환해서 영상 처리를 진행합니다.

이미지 피라미드는 가우시안 피라미드(Gaussian Pyramid)와 라플라시안 피라미드(Laplacian pyramid)를 활용합니다.

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
            Mat src = new Mat("tree.jpg", ImreadModes.ReducedColor2);
            Mat pyrUp = new Mat();
            Mat pyrDown = new Mat();

            Cv2.PyrUp(src, pyrUp);
            Cv2.PyrDown(src, pyrDown);

            Cv2.ImShow("pyrUp", pyrUp);
            Cv2.ImShow("pyrDown", pyrDown);
            Cv2.WaitKey(0);
        }
    }
}
```

## 세부 코드

```c#
Mat src = new Mat("tree.jpg");
Mat pyrUp = new Mat();
Mat pyrDown = new Mat();
```
new Mat을 사용해 이미지를 src에 할당합니다.

pyrUp은 확대된 이미지를 저장할 변수입니다.

pyrDown은 축소된 이미지를 저장할 변수입니다.

>Tip : Mat 클래스를 기본 생성자로 할당할 경우, 클래스나 함수에서 자동으로 속성을 할당합니다.

```c#
Cv2.PyrUp(src, pyrUp);      // 4배 확대
Cv2.PyrDown(src, pyrDown);  // 4배 축소
```
확대 함수(Cv2.PyrUp) 또는 축소 함수(Cv2.PyrDown)를 활용해 이미지를 변환합니다.

Cv2.Pyr*(원본 이미지, 결과 이미지, 결과 이미지 크기, 테두리 외삽법)으로 이미지 크기를 변환합니다.

결과 이미지 크기는 매개변수에 직접 인수를 할당해서 (업/다운)샘플링을 수행할 수 있습니다.

테두리 외삽법은 확대 또는 축소할 경우, 영역 밖의 픽셀은 추정해서 값을 할당해야합니다.

이미지 밖의 픽셀을 외삽하는데 사용되는 테두리 모드입니다. 외삽 방식을 설정합니다.

## 테두리 외삽법 종류

|속성                           |의미                       |
|-------------------------------|---------------------------|
|InterpolationFlags.Nearest	    |가장 가까운 이웃 보간법    |
|InterpolationFlags.Linear	    |*쌍 선형 보간법*           |
|InterpolationFlags.Area	    |영역 보간법                |
|InterpolationFlags.Cubic	    |4×4 바이 큐빅 보간법       |
|InterpolationFlags.Lanczos4	|8×8 란초스 보간법          |

## 출력 결과