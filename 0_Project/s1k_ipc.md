# < IPC 포멧 >

|< `Packet`의 구성 >|||||||
|-|-|-|-|-|-|-|
| 구성요소 5가지            | `Packet ID`| `Main Type` | `Sub Type` | `Length` | `Data`           | 
| `Control Path`           | 5 Bytes    | 1 Bytes     | 2 Bytes    | 4 Bytes  | 192 Bytes(max)   |
| `Image Delivery Path`    | 5 Bytes    | 1 Bytes     | 2 Bytes    | 24 Bytes | 30624 Bytes(max) |
| `UDP Path`               | 5 Bytes    | 1 Bytes     | 2 Bytes    | 4 Bytes  | 192 Bytes(max)   |

<br>

### 1. `Packet ID(5Bytes)` - 인식자, Identifier

+ `Packet ID(5Bytes)` = `Start of Packet`(2Bytes) + `송신 Device ID`(1Bytes) + `수신 Device ID`(1Bytes) + `Handshake`(1Bytes)
   

    || `Start of Packet` | `송신 Device` | `수신 Device` | `Handshake` |
    |-|-|-|-|-|
    | 크기 | 2 Bytes  | 1 Bytes |  1 Bytes |  1 Bytes | 
    | 값   | [0xFFFF] | pc : [0x00]<br> smart Camera : [0x01] ~ [0xFE] |  pc : [0x00]<br> smart Camera : [0x01] ~ [0xFE] |  [0xFF]<br> Response : ACK(0x00), NACK(0x01), Command SKIP(0x02) | 
    | 설명 |패킷 시작은 `0xFFFF` | 컴퓨터는 `0x00` <br> 카메라는 `0x01` 부터 | 컴퓨터는 `0x00` <br> 카메라는 `0x01` 부터 | 

<br>

### 2. `Main(1Bytes)` - 주 색인 (Packet의 `목적`은 뭔가? ex. `인터페이스`를 수정한다.)

+ [0x01] (page 12) : Interface Configure (인터페이스 구성) 
+ [0x02] (page 19) : Platform Version
+ [0x03] (page 22) : Image Frame Configure (이미지 프레임 구성)
+ [0x04] (page 29) : Illumination Controller Configure (조명 컨트롤러 구성)
+ [0x05] (page 30) : I/O
+ [0x06] (page 34) : File Management
+ [0x07] (page 48) : File Transfer PtoS
+ [0x08] (page 49) : File Transfer StoP
+ [0x09] (page 50) : Operation Result
+ [0x0A] (page 52) : Operation Result

<br>

### 3. `Sub(2Bytes)` - 보조 색인 (ex. `인터페이스`에서 `IP`를 수정한다.)

<br>

### 4. `Length` - Data의 길이
- `Length` 뒤에 따라오는 `Data`의 `길이`를 나타낸다.

<br>

### 5. `DATA`

<br>

---

<br>

## < Image 수신 방법 > 

|                          | `Packet ID`| `Main Type` | `Sub Type` | `Length` | `Data`           | 
|-                         |-           |-            |-           |-         |-                 |
| `Image Delivery Path`    | 5 Bytes    | 1 Bytes     | 2 Bytes    | 24 Bytes | 30624 Bytes(max) |
| 5000번 port 신호         |             | 0x06       | 0x0006     | 1        | 

- 5000번 port로 신호를 보내게 되면
- 5000번 port로 응답이 오고
    - 정상적인 신호를 보내면 `Handshake`가 `0xFF` -> `0x00`으로 바뀌어 수신이 된다. 
- 5001번 port로 Image를 수신하게 된다. 