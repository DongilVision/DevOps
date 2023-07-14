# **Chapter18. 윤곽선 관련 함수(1)**

## **개요**
OpenCvSharp에서는 검출된 윤곽선의 형상을 **분석 및 재가공**할 때, 사용할 수 있는 함수를 제공한다. 검출된 윤곽선의 정보를 활용하여 파생될 수 있는 정보를 제공한다.

윤곽선 객체의 `중심점`, `길이`, `넓이`, `최소 사각형` 등의 윤곽선 정보를 통해 계산할 수 있는 정보들을 쉽게 구할 수 있다.

## **18.1. 프로그램 작성**

### **18.1.1. 이미지 및 코드**

예제 이미지는 17장과 동일하며, 코드 또한 17장의 코드에서 시작

```cs
using System;
using OpenCvSharp;
using System.Collections.Generic;

namespace Project {
    class Program {
        static void Main(string[] args) {
            Mat src = new Mat("hex.jpg");
            Mat yellow = new Mat();
            Mat dst = src.Clone();

            Point[][] contours;
            HierarchyIndex[] hierarchy;

            Cv2.InRange(src, new Scalar(0, 127, 127), new Scalar(100, 255, 255), yellow);
            Cv2.FindContours(yellow, out contours, out hierarchy, RetrievalModes.Tree, ContourApproximationModes.ApproxTC89KCOS);

            List<Point[]> new_contours = new List<Point[]>();

            foreach(Point[] p in contours) {
                double length = Cv2.ArcLength(p, true);
                if(length > 100) {
                    new_contours.Add(Cv2.ApproxPolyDP(p, length * 0.02, true));
                }
            }

            Cv2.DrawContours(dst, new_contours, -1, new Scalar(255, 0, 0), 2, LineTypes.AntiAlias, null, 1);

            Cv2.ImShow("src", src);
            Cv2.ImShow("dst", dst);
            Cv2.WaitKey(0);
        }
    }
}
```

### **18.1.2. 수정 사항**

윤곽선 관련 함수 알고리즘은 `하나의 윤곽선을 대상으로 진행`되므로, 기존 코드와 동일하게 **foreach(반복문)** 을 사용하여, 개별의 윤곽선으로부터 정보를 계산한다.

#### **18.1.2.1. 윤곽선 면적 함수**

```cs
// List<Point[]> new_contours = new List<Point[]>(); 삭제
foreach(Point[] p in contours) {
    double length = Cv2.ArcLength(p, true);
    double area = Cv2.ContourArea(p, true); // 추가: 윤곽선 넓이 함수

    ...
}
```

윤곽선 넓이 함수 `Cv2.ContourArea(윤곽선 배열, 폐곡선 여부)`로 윤곽선의 면적을 계산한다. **폐곡선 여부**는 시작점과 끝점의 연결 여부를 의미한다. `true`대입 시, 마지막 점과 시작 점이 연결된 것으로 간주한다. 폐곡선 여부에 따라 결과값이 상이하게 발생된다.

#### **18.1.2.2. 유의미한 정보만 계산**

```cs
// if(length > 100) new_contours.Add(Cv2.ApproxPolyDP(p, length * 0.02, true)); 삭제
if(length < 100 && area < 1000 && p.Length < 5) continue;
```
* `length`: 윤곽선의 길이
* `area`: 윤곽선의 면적
* `p.Length`: 윤곽선을 이루는 윤곽점의 개수

\* **윤곽선의 길이가 100미만**, **면적이 1000 미만**, **윤곽점의 개수가 5개 미만**인 윤곽선은 `무시`한다.

#### **18.1.2.3. 경계 사각형 함수**

```cs
// Cv2.BoundingRect() return type: Rect
Rect boundingRect = Cv2.BoundingRect(p);
```
윤곽선의 경계면을 둘러싸는 사각형을 계산하는 함수인 `Cv2.BoundingRect(윤곽선 배열)`는 대입된 윤곽선 배열에 대한 **최소 크기의 사각형**을 계산한다.

#### **18.1.2.4. 최소 면적 사각형 함수**

```cs
// Cv2.MinAreaRect() return type: RotatedRect
RotatedRect rotatedRect = Cv2.MinAreaRect(p);
```

최소 면적 사각형 함수 `Cv2.MinAreaRect()`는 윤곽선의 경계면을 둘러싸는 **최소 크기의 사각형**을 계산한다.

\* `Cv2.BoundingRect()`와 `Cv2.MinAreaRect()` 모두 주어진 객체 또는 윤곽선을 감싸는 최소 크기의 사각형을 계산하는 데 사용되나, `Cv2.BoundingRect()`는 최소 크기의 **수직 사각형**을 반환하고, `Cv2.MainAreaRect()`는 **수직 사각형**이 아닌 **회전된 사각형(RotatedRect)**을 반환한다는 차이점이 있다.

