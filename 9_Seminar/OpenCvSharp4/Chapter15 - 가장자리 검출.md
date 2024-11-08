# 15장 - 가장자리 검출

## 가장자리 검출 (Edge Detection)

![?](./Source/wintry.jpg)

`가장자리(Edge)`는 `객체의 가장 바깥 부분의 둘레`를 의미하며, `객체의 테두리`로 볼 수 있습니다.

이미지 상에서 가장자리는 전경(foreground)과 배경(background)이 구분되는 지점이며, 
전경과 배경 사이에서 `밝기가 큰 폭으로 변하는 지점`이 객체의 `가장자리`가 됩니다.

그러므로 가장자리는 `픽셀의 밝기가 급격하게 변하는 부분`으로 간주할 수 있습니다. 
즉, 픽셀의 `밝기 변화율(Rate of change)이 높은 부분`이 가장자리가 됩니다.

가장자리 검출 함수는 크게  `소벨 미분`, `샤르 필터`, `라플라시안`, `캐니 엣지`가 있습니다.


## 미분 (Derivation)

![?](./Source/Derivative.jpg)

가장자리 검출은 주로 `1차 미분`이나 `2차 미분`을 이용해 `변화율이 높은` 지점을 가장자리로 간주합니다.

그러므로 미분을 진행할 경우 `노이즈에 큰 영향`을 받아, `흐림 효과를 진행`한 다음 가장자리를 검출합니다.

또한, 이미지는 샘플링과 양자화가 처리된 데이터이므로 밝기의 평균변화율이 아닌 밝기의 순간변화율을 구해 계산합니다.

## 메인 코드
```cs
            // 객체 선언
            Mat src = new Mat("wintry.jpg");
            Mat blur = new Mat();

            Mat sobel = new Mat();
            Mat scharr = new Mat();
            Mat laplacian = new Mat();
            Mat canny = new Mat();

            // 가우시안 필터 적용
            Cv2.GaussianBlur(src, blur, new Size(3, 3), 1, 0, BorderTypes.Default);

            // 가장자리 검출

                //Sobel (소벨)
            Cv2.Sobel(blur, sobel, MatType.CV_32F, 1, 0, ksize: 3, scale: 1, delta: 0, BorderTypes.Default);
            sobel.ConvertTo(sobel, MatType.CV_8UC1);
            
                //Scharr (샤르)
            Cv2.Scharr(blur, scharr, MatType.CV_32F, 1, 0, scale: 1, delta: 0, BorderTypes.Default);
            scharr.ConvertTo(scharr, MatType.CV_8UC1);

                //Laplacian (라플라시안)
            Cv2.Laplacian(blur, laplacian, MatType.CV_32F, ksize: 3, scale: 1, delta: 0, BorderTypes.Default);
            laplacian.ConvertTo(laplacian, MatType.CV_8UC1);

                //Canny (케니)
            Cv2.Canny(blur, canny, 100, 200, 3, true);

            // 출력
            Cv2.ImShow("sobel", sobel);
            Cv2.ImShow("scharr", scharr);
            Cv2.ImShow("laplacian", laplacian);
            Cv2.ImShow("canny", canny);
            Cv2.WaitKey(0);
```

## 세부 코드
```cs
Mat src = new Mat("wintry.jpg");
Mat blur = new Mat();

Mat sobel = new Mat();
Mat scharr = new Mat();
Mat laplacian = new Mat();
Mat canny = new Mat();
```
new Mat을 사용해 이미지를 src에 할당합니다.

흐림 효과 결과를 저장할 blur를 선언합니다.

연산 결과를 저장할 sobel, scharr, laplacian, canny를 선언합니다.



### < 먼저 Blur 적용 >
```cs
Cv2.GaussianBlur(src, blur, new Size(3, 3), 1, 0, BorderTypes.Default);
```

가우시안 흐림 효과 함수(Cv2.GaussianBlur)는 이미지의 각 지점에 가우시안 커널을 적용해 합산한 후에 출력 이미지를 반환합니다.

`원본 이미지에 가장자리 검출 함수를 적용하는 것이 아닌`, `흐림 효과가 적용된 이미지`에 `연산을 진행`하기 위해 적용합니다.



### < Sobel 소벨 >
![?](./Source/sobel.png)
```cs
Cv2.Sobel(blur, sobel, MatType.CV_32F, 1, 0, ksize: 3, scale: 1, delta: 0, BorderTypes.Default);
sobel.ConvertTo(sobel, MatType.CV_8UC1);
```
`소벨 미분 함수(Cv2.Sobel)`는 `미분 값을 구할 때 가장 많이 사용되는 연산자`입니다.

Cv2.Sobel(원본 배열, 결과 배열, 결과 배열 정밀도, X 방향 미분 차수, Y 방향 미분 차수, 커널, 비율, 오프셋, 테두리 외삽법)로 소벨 미분을 적용합니다.

입력 이미지가 8비트의 정밀도를 갖는 경우 오버플로가 발생할 수 있어 16비트 이상의 정밀도를 결과 배열의 정밀도로 사용합니다.

차수는 0, 1, 2를 사용하며, 두 차수의 합은 1 이상이 돼야 합니다.

커널은 홀수 값만 사용할 수 있으며, 31까지의 크기만 지원합니다.

비율과 오프셋은 출력 이미지를 반환하기 전에 계산되며, 8비트 정밀도의 이미지를 사용해 이미지를 시각적으로 확인하고자 할 때 조절값으로 사용합니다.

테두리 외삽법은 컨벌루션 연산이므로, 이미지 가장자리 부분의 계산 방법을 설정합니다.

ConvertTo 함수는 이미지 출력 함수(Cv2.Imshow)가 8비트 이미지만 지원하므로 출력을 위해 변환합니다.

원본 배열.ConvertTo(결과 배열, 반환 형식)으로 사용합니다.



### < Scharr 샤르 >
![?](./Source/Scharr.png)
```cs
Cv2.Scharr(blur, scharr, MatType.CV_32F, 1, 0, scale: 1, delta: 0, BorderTypes.Default);
scharr.ConvertTo(scharr, MatType.CV_8UC1);
```

`샤르 필터 함수(Cv2.Scharr)`는 `소벨 미분의 단점을 보완한 방식`입니다.

Cv2.Scharr(원본 배열, 결과 배열, 결과 배열 정밀도, X 방향 미분 차수, Y 방향 미분 차수, 비율, 오프셋, 테두리 외삽법)로 샤르 필터를 적용합니다.

`소벨 미분`의 경우 `커널의 크기가 작으면` `정확도가 떨어`지는데, 크기가 작은 3×3의 소벨 미분의 경우 기울기(Gradient)의 각도가 수평이나 수직에서 멀어질수록 정확도가 떨어집니다.

이를 보완하고자 샤르 필터를 사용합니다. `샤르 필터는 커널의 크기가 3x3 크기만 지원`합니다.

ConvertTo 함수는 이미지 출력 함수(Cv2.Imshow)가 8비트 이미지만 지원하므로 출력을 위해 변환합니다.

원본 배열.ConvertTo(결과 배열, 반환 형식)으로 사용합니다.



### < Laplacian 라플라시안 >
![?](./Source/laplacian.png)
```c#
Cv2.Laplacian(blur, laplacian, MatType.CV_32F, ksize: 3, scale: 1, delta: 0, BorderTypes.Default);
laplacian.ConvertTo(laplacian, MatType.CV_8UC1);
```

`라플라시안 함수(Cv2.GaussianBlur)`는 `2차 미분의 형태로 반환`합니다.

라플라시안 함수는 가장자리가 밝은 부분에서 발생한 것인지, 어두운 부분에서 발생한 것인지 알 수 있습니다.

Cv2.Laplacian(원본 배열, 결과 배열, 결과 배열 정밀도, 커널, 비율, 오프셋, 테두리 외삽법)로 라플라시안을 적용합니다.

2차 미분 방식은 x축과 y축을 따라 2차 미분한 합을 의미합니다.

커널의 크기가 1일 때는 라플라시안 단일 커널을 적용해 계산합니다.

ConvertTo 함수는 이미지 출력 함수(Cv2.Imshow)가 8비트 이미지만 지원하므로 출력을 위해 변환합니다.

원본 배열.ConvertTo(결과 배열, 반환 형식)으로 사용합니다.



### < Canny Edge  케니 엣지>
![?](./Source/canny.png)
```c#
Cv2.Canny(blur, canny, 100, 200, 3, true);
```
`캐니 엣지(Canny Edge)`는 `라플라스 필터 방식을 캐니(J. Canny)가 개선한 방식`으로서 x와 y에 대해 1차 미분을 계산한 다음, 네 방향으로 미분합니다.

#### - 캐니 엣지 알고리즘 동작 순서는 다음과 같습니다.

```c#
1.	노이즈 제거를 위해 가우시안 필터를 사용해 흐림 효과를 적용
2.	기울기(Gradient) 값이 높은 지점을 검출(소벨 마스크 적용)
3.	최댓값이 아닌 픽셀의 값을 0으로 변경(명백하게 가장자리가 아닌 값을 제거)
4.	히스테리시스 임곗값(hysteresis threshold) 적용
```

Cv2.Canny(원본 배열, 결과 배열, 하위 임곗값, 상위 임곗값, 소벨 연산자 크기, L2 그레이디언트)로 캐니 엣지를 적용합니다.

하위 임곗값은 픽셀 값이 하위 임곗값보다 낮은 경우 가장자리로 고려하지 않습니다.

상위 임곗값은 픽셀이 상위 임곗값보다 큰 기울기를 가지면 픽셀을 가장자리로 간주합니다.

상위 임곗값보다 낮으면서 하위 임곗값보다 높은 경우 상위 임곗값에 연결된 경우만 가장자리 픽셀로 간주합니다.

즉, 상위 임곗값이 200, 하위 임곗값이 100일 경우 100 이하의 픽셀은 모두 제외되며 200 이상의 값을 하나라도 포함하고 있는 100 이상의 모든 픽셀은 가장자리로 간주합니다.

캐니 엣지도 소벨 연산에 기반을 두고 있으므로 소벨 연산자 마스크 크기(apertureSize)를 설정합니다.

L2 그레이디언트(L2gradient)는 L2-norm으로 방향성 그레이디언트를 정확하게 계산할지, 정확성은 떨어지지만 속도가 더 빠른 L1-norm으로 계산할지를 선택합니다.

