# 제 22장 - 원근 변환

<br>

## 원근 변환(Perspective Transformation)

<img src="./Source/plate.jpg" width="49%"> <img src="./Source/plateChange.jpg" width="49%">

`원근 변환(Perspective Transformation)`은 원근감을 표현하기 위한 변환입니다.

아핀 변환과 비슷하지만 `선의 수평성을 유지하지 않`고, `직선의 성질만 유지`되며 사각형을 임의의 사각형 형태로 변환하는 것을 의미합니다.

원근 변환은 `뒤틀림`이나 `원근 왜곡`을 표현해야 하므로 `아핀 변환에 비해 더 많은 미지수를 요구`합니다.

<br>

## 원근 변환 행렬(Perspective Transformation Matrix)

<img src="./Source/PerspectiveTransformationMatrix.jpg" width="50%">

원근 변환 행렬은 아핀 변환 행렬과 비슷한 형태를 지닙니다.

아핀 변환 행렬과 차이점은 0, 0, 1의 행에서 a20, a21, 1로 변경되어, 여섯 개의 미지수에서 여덟 개의 미지수가 됩니다.

행렬의 x1, y1은 변환 전 원본 이미지의 픽셀 좌표를 의미하며, 

x2, y2는 변환 후의 결과 이미지의 픽셀 좌표를 의미합니다.

변환 후의 픽셀 좌표를 게산하기 위해서는 미지수 a00, a01, a10, a11, a20, a21, b0, b1의 값을 알아야 합니다.

여덟 개의 미지수를 구하기 위해 네 개의 좌표를 활용해 미지수를 계산합니다.

<br>

## 메인 코드 - `WarpPerspective()`

```cs
            Mat src = new Mat("plate.jpg");
            Mat dst = new Mat();

            // 아핀 맵 행렬 생성
            List<Point2f> src_pts = new List<Point2f>()     // 변환 전 4개 픽셀 좌표
            {
                new Point2f(0.0f, 0.0f),
                new Point2f(0.0f, src.Height),
                new Point2f(src.Width, src.Height),
                new Point2f(src.Width, 0.0f)
            };

            List<Point2f> dst_pts = new List<Point2f>()     // 변환 후 4개 픽셀 좌표
            {
               new Point2f(300.0f, 100.0f),
               new Point2f(300.0f, src.Height),
               new Point2f(src.Width - 400.0f, src.Height - 200.0f),
               new Point2f(src.Width - 200.0f, 200.0f)
            };

            // 원근 맵 행렬 생성 함수
            Mat matrix = Cv2.GetPerspectiveTransform(src_pts, dst_pts);

            // 생성된 원근 맵 행렬로 원근 변환 진행
            Cv2.WarpPerspective(src, dst, matrix, new Size(src.Width, src.Height));

            Cv2.ImShow("dst", dst);
            Cv2.WaitKey(0);         
```

<img src="./Source/plateChangeHow.png">

<br>

## 세부 코드

```cs
Mat src = new Mat("plate.jpg");
Mat dst = new Mat();
```

new Mat을 사용해 이미지를 src에 할당합니다.

연산 결과를 저장할 dst를 선언합니다.

```cs
List<Point2f> src_pts = new List<Point2f>()
{
    new Point2f(0.0f, 0.0f),
    new Point2f(0.0f, src.Height),
    new Point2f(src.Width, src.Height),
    new Point2f(src.Width, 0.0f)
};

List<Point2f> dst_pts = new List<Point2f>()
{
    new Point2f(300.0f, 100.0f),
    new Point2f(300.0f, src.Height),
    new Point2f(src.Width - 400.0f, src.Height - 200.0f),
    new Point2f(src.Width - 200.0f, 200.0f)
};

Mat matrix = Cv2.GetPerspectiveTransform(src_pts, dst_pts);
```

원근 변환을 진행하기 위해선, 원근 맵 행렬을 생성해야 합니다.

원근 맵 행렬 생성 함수(Cv2.GetPerspectiveTransform)는 변환 전 네 개의 픽셀 좌표(src_pts)와 변환 후 네 개의 픽셀 좌표(dst_pts)를 이용해 원근 맵 행렬(matrix)을 생성합니다.

Cv2.GetPerspectiveTransform(변환 전 픽셀 좌표, 변환 후 픽셀 좌표)로 원근 맵 행렬을 생성합니다.

픽셀 좌표는 4개의 픽셀 좌표를 포함해야 하므로, 목록(List)을 통해, Point2f 형식의 좌표를 생성합니다.

src_pts와 dst_pts의 픽셀 좌표들의 순서는 1:1로 매칭됩니다.

```cs
Cv2.WarpPerspective(src, dst, matrix, new Size(src.Width, src.Height));
```

생성된 원근 행렬을 활용해 원근 변환을 진행합니다.

원근 변환 함수(Cv2.WarpPerspective)는 원근 행렬을 사용해 변환된 이미지를 생성합니다.

Cv2.WarpPerspective(원본 배열, 결과 배열, 행렬, 결과 배열의 크기, 보간법, 테두리 외삽법, 테두리 색상)로 아핀 변환을 진행합니다.

결과 배열의 크기를 설정하는 이유는 회전 후, 원본 배열의 이미지 크기와 다를 수 있기 때문입니다.

이미지를 더 큰 공간에 포함하거나, 더 작은 공간에 포함할 수 있습니다.

그러므로, 결과 배열의 크기를 새로 할당하거나, 원본 배열의 크기와 동일하게 사용합니다.

보간법, 테두리 외삽법, 테두리 색상 또한, 새로운 공간에 이미지를 할당하므로, 보간에 필요한 매개변수들을 활용할 수 있습니다.