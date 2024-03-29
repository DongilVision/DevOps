# **Chapter02. <u>Mat</u> 클래스**

## < Mat 클래스 >
> Mat 클래스는 Matrix의 약자로 행렬을 표현하기 위한 데이터 형식입니다.

> C++ 스타일의 <u>N차원 고밀도 배열 클래스</u>이며, 행렬(2차원)을 비롯해 배열(1, 2, 3차원)을 효율적으로 표현할 수 있습니다.

> Mat 클래스는 <u>헤더(Header)</u>와 <u>데이터 포인터(Data Pointer)</u>로 구성되어 있습니다.

> 헤더는 Mat 클래스에 대한 정보가 담겨 있습니다. 즉, <u>행렬의 크기</u>나 <u>행렬의 깊이</u> 등이 저장됩니다.

> 데이터 포인터는 각 데이터가 담겨 있는 메모리 주소 정보가 저장되어 있습니다.

***

## < Mat 클래스 구성 요소 >
Mat 클래스는 크게 세 가지의 구조로 이뤄져있습니다.

<u>행렬의 크기</u>, <u>데이터 타입</u>, <u>깊이(채널)</u>입니다. 구조의 의미는 다음과 같습니다.
1. 행렬의 크기 : 행(높이)과 열(너비) 크기
2. 데이터 타입 : 행렬의 각 요소에 대한 데이터 타입
3. 깊이(채널) : 행렬의 깊이(채널)

***

## < 네임스페이스 추가>
```C#
using OpenCvSharp;  
```
OpenCV4의 <u>데이터 형식</u>이나 <u>함수 및 메서드</u>를 사용하기 위해 네임스페이스에 using OpenCvSharp;을 추가합니다.

Mat 클래스 또한 using OpenCvSharp;에 포함되어 있습니다.

+ Tip : 모호한 참조가 발생했을 때, OpenCvSharp.*의 형태로 함수나 메서드를 호출해 사용합니다.

+ Tip : 추가적인 기능이 포함된 확장 네임스페이스를 사용하기 위해서는 using OpenCvSharp.*;의 형태로 등록합니다.

***

## < Mat 클래스 생성 >
```C#
Mat src = new Mat();
```
Mat 클래스는 생성자를 인스턴스화 하는 순간 행렬이 생성됩니다.

기본 생성자의 경우, 행렬의 크기와 데이터 타입은 존재하지 않습니다.

```C#
Mat src1 = new Mat(new Size(640, 480), MatType.CV_8UC3);
Mat src2 = new Mat(480, 640, MatType.CV_8UC3);
```

Mat 클래스의 일반적인 생성 형태는 위와 같습니다.

행렬의 크기는 Size 구조체를 사용하거나 행과 열에 값을 직접 입력하는 식으로 할당이 가능합니다.

데이터 타입과 깊이(채널)은 MatType.*을 사용해 할당이 가능합니다.

MatType은 <u>CV_AABB의 구조</u>를 가집니다. <u>AA는 데이터 타입</u>을 의미하며, <u>BB는 깊이(채널)</u>을 의미합니다.
> < 데이터 타입 >
>
>CV_8U : uchar, usigned char
>
>CV_8S : schar, signed char
>
>CV_16U : ushort, unsigned short
>
>CV_16S : signed short
>
>CV_32S : int
>
>CV_32F : float
>
>CV_64F : double
>
>CV_16F : float16_t


<u>8U</u>는 <u>unsigned 8-bit integers</u>를 의미하며, <u>C3</u>는 <u>3채널</u>을 의미합니다.

***
### - 자료형 매크로 상수 표기법 
Mat 클래스에서는 행렬이 어떤 자료형을 사용하는 지에 대한 정보를 깊이라고 합니다.

Mat 행렬의 깊이를 다음과 같은 형식의 매크로 상수를 이용하여 표현합니다.



***

### - Mat 클래스 생성자

```C#
public Mat();                                       // 빈 매트에서 생성
public Mat(IntPtr ptr);                             // 포인터에서 생성
public Mat(Mat m, Rect roi);                        // Rect 구조체 사용.
public Mat(Mat m, params Range[] ranges);           // Range 구조체 사용
public Mat(Size size, MatType type);                // 지정된 크기 및 유형의 2D 행렬 구성
public Mat(IEnumerable<int> sizes, MatType type);   // N차원 행렬을 구성
public Mat(string fileName, ImreadModes flags = ImreadModes.Color); // 파일에서 이미지 로드
public Mat(Size size, MatType type, Scalar s);  //2D 매트릭스를 구성하고 지정된 스칼라 값으로 채움
public Mat(Mat m, Range rowRange, Range? colRange = default(Range?));   
public Mat(IEnumerable<int> sizes, MatType type, Scalar s); // N차원 행렬 구성
public Mat(int rows, int cols, MatType type);   //지정된 크기 및 유형의 2D행렬을 구성.
public Mat(int rows, int cols, MatType type, Scalar s); //지정된 크기 및 유형의 2D행렬 구성후 scalar로 채움

//사용자 할당 데이터를 가리키는 행렬 헤더의 생성자
public Mat(IEnumerable<int> sizes, MatType type, IntPtr data, IEnumerable<long> steps = null);
public Mat(IEnumerable<int> sizes, MatType type, Array data, IEnumerable<long> steps = null);
public Mat(int rows, int cols, MatType type, IntPtr data, long step = 0);
public Mat(int rows, int cols, MatType type, Array data, long step = 0);
```
Mat 클래스는 위와 같은 형태로도 사용할 수 있습니다.

Size 구조체, Range 구조체, Rect 구조체, Scalar 구조체, 배열, 열거자, 포인터 등을 사용해 생성할 수 있습니다.

또한, 외부의 파일을 불러와 이미지를 Mat 클래스에 할당해 사용할 수 있습니다.

Mat 클래스는 기본적으로 이미지(행렬)을 표시하기 위한 데이터 형식입니다.

+ Tip : Mat 클래스는 래스터 주사 순서를 따릅니다.

+ Tip : Mat 클래스는 행렬 표현식(MatExpr 클래스), 희소 행렬(SparseMat 클래스) 등도 호환이 가능합니다.