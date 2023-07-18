# 제 20장 - 회전

<br>

## 이미지 회전(Image Rotation)

<img src="./Source/wine.jpg" width="49%"> <img src="./Source/WineChanged.jpg" width="49%">


`이미지 회전`은 강체 변환(Rigid Transformation)과 유사 변환(Similarity Transformation)에 포함되는 변환 중 하나입니다.

이미지 회전은 두 가지의 변환에 포함되는데, 등방성(Isotropic) 크기 변환의 유/무로 변환의 방식의 결정됩니다.

`강체 변환`은 `변환의 기준점으로부터 크기와 각도가 보존되는 변환`입니다.

`유사 변환`은 `강체 변환에 등방성 크기 변환이 추가된 변환`입니다.

즉, `단순한 회전`의 경우 `강체 변환`이며, `크기가 변환되면서 회전`한다면 `유사 변환`이 됩니다.  
  
<br>

## 2×2 회전 행렬(2×2 Rotation Matrix)  : 단순한 회전

<img src="./Source/좌표의 회전 이동.jpg" width="48%" height="50%"> <img src="./Source/좌표축의 회전 이동.jpg" width="48%" height="50%">

회전 행렬에는 크게 두 가지 종류가 있습니다.

좌표의 값을 회전시키는 `좌표 회전 행렬`과 좌표축을 회전시키는 `좌표축 회전 행렬`이` 있습니다.

`좌표 회전 행렬`은 원점을 중심으로 `좌푯값을 회전시켜 매핑`합니다.

`좌표축 회전 행렬`은 원점을 중심으로 `행렬 자체를 회전`시켜 `새로운 행렬의 값`을 구성합니다.

두 회전 행렬 모두 원점을 중심으로 계산을 진행합니다.

<br>

## 2×3 회전 행렬(2×3 Rotation Matrix) : 임의의 중심점 기반 -> 기준점 변경 및 비율 조정 가능

<img src="./Source/회전행렬.jpg" width="50%" height="50%">

단순한 회전은 2×2 행렬을 활용해 원하는 결과를 쉽게 얻을 수 있습니다.

하지만, 임의의 중심점을 기반으로 회전을 수행하기 위해서는 `아핀 변환(Affine Transformation)에 기반을 둔 회전 행렬을 활용`해야 합니다.

2×3 회전 행렬을 사용할 경우 `회전 축의 기준점 변경`과 `비율`을 조정할 수 있다.

`Center`는 중심점의 좌표, `scale`은 비율, `θ`는 회전 각도를 의미합니다.

이 회전 행렬은 부동 소수점의 형태로 반환합니다.

<br>

## 메인 코드

```cs
            Mat src = new Mat("wine.jpg");
            Mat dst = new Mat();

            // 회전행렬 생성. GetRotationMartix2D => 회전 행렬 생성 함수 
            Mat matrix = Cv2.GetRotationMatrix2D(new Point2f(src.Width / 2, src.Height / 2),    45.0   ,  1.0 );
            //                                  (                중심점 좌료               , 회전 각도 , 비율 );

            // 아핀변환 진행 
            Cv2.WarpAffine(src , dst  , matrix , new Size(src.Width, src.Height));
            //            (원본, 결과 , 행렬   , 결과 배열 크기                 );  

            Cv2.ImShow("dst", dst);
            Cv2.WaitKey(0);
```

<br>

## 세부 코드

```cs
Mat src = new Mat("wine.jpg");
Mat dst = new Mat();
```

new Mat을 사용해 이미지를 src에 할당합니다.

연산 결과를 저장할 dst를 선언합니다.

<br>

```cs
Mat matrix = Cv2.GetRotationMatrix2D(new Point2f(src.Width / 2, src.Height / 2), 45.0, 1.0);
```
이미지를 회전시키기 위해, 회전 행렬을 생성합니다.

2×3 회전 행렬 생성 함수(Cv2.GetRotationMatrix2D)는 Mat 형식의 회전 행렬을 생성합니다.

Cv2.GetRotationMatrix2D(중심점의 좌표, 회전 각도, 비율)로 회전 행렬을 생성합니다.

중심점의 좌표를 기준으로 회전 각도만큼 회전하며, 비율만큼 크기를 변경합니다.

<br>

```cs
Cv2.WarpAffine(src, dst, matrix, new Size(src.Width, src.Height));
```
생성된 회전 행렬을 활용해 아핀 변환을 진행합니다.

아핀 변환 함수(Cv2.WarpAffine)는 회전 행렬을 사용해 회전된 이미지를 생성합니다.

Cv2.WarpAffine(원본 배열, 결과 배열, 행렬, 결과 배열의 크기)로 회전 행렬을 생성합니다.

결과 배열의 크기를 설정하는 이유는 회전 후, 원본 배열의 이미지 크기와 다를 수 있기 때문입니다.

만약, 45° 이미지를 회전한다면, 사각형 프레임 안에 포함시켜야 합니다.

그로 인해 이미지를 더 큰 공간에 포함하거나, 더 작은 공간에 포함할 수 있습니다.

그러므로, 결과 배열의 크기를 새로 할당하거나, 원본 배열의 크기와 동일하게 사용합니다.

