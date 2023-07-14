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
                if(length > 100) new_countours.Add(p);
            }

            Cv2.DrawContours(dst, new_contours, -1, new Scalar(255, 0, 0), 2, LineTypes.AntiAlias, null, 1);

            Cv2.ImShow("src", src);
            Cv2.ImShow("dst", dst);
            Cv2.WaitKey(0);
        }
    }
}
```