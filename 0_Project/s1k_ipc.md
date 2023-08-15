### IPC
* S1000 IPC는 영상등 각종 파라메터를 제어하기 위하여 사용된다.
* 인식자(8바이트) + (값길이,값) 으로 구성된다.
* 인식자는 PacketID, MainCode, SubCode 로구성된다.
* SET/GET으로 구성된다.
 

<br>

|< Packet의 구성 >||||||
|-|-|-|-|-|-|
| 구성요소 5가지            | Packet ID| Main Type | Sub Type | Length | Data           | 
| Control Path           | 5 Bytes    | 1 Bytes     | 2 Bytes    | 4 Bytes  | 192 Bytes(max)   |
| Image Delivery Path    | 5 Bytes    | 1 Bytes     | 2 Bytes    | 24 Bytes | 30624 Bytes(max) |
| UDP Path               | 5 Bytes    | 1 Bytes     | 2 Bytes    | 4 Bytes  | 192 Bytes(max)   |

<br>

### 1. Packet ID(5Bytes) - 인식자, Identifier

+ Packet ID(5Bytes) = Start of Packet(2Bytes) + 송신 Device ID(1Bytes) + 수신 Device ID(1Bytes) + Handshake(1Bytes)
   

    || Start of Packet | 송신 Device | 수신 Device | Handshake |
    |-|-|-|-|-|
    | 크기 | 2 Bytes  | 1 Bytes |  1 Bytes |  1 Bytes | 
    | 값   | [0xFFFF] | pc : [0x00]<br> smart Camera : [0x01] ~ [0xFE] |  pc : [0x00]<br> smart Camera : [0x01] ~ [0xFE] |  [0xFF]<br> Response : ACK(0x00), NACK(0x01), Command SKIP(0x02) | 
    | 설명 |패킷 시작은 0xFFFF | 컴퓨터는 0x00 <br> 카메라는 0x01 부터 | 컴퓨터는 0x00 <br> 카메라는 0x01 부터 | 

<br>

### 2. Main(1Bytes) - 주 색인 (Packet의 목적은 뭔가? ex. 인터페이스를 수정한다.)

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

### 3. Sub(2Bytes) - 보조 색인 (ex. 인터페이스에서 IP를 수정한다.)

<br>

### 4. Length - Data의 길이
- Length 뒤에 따라오는 Data의 길이를 나타낸다.

<br>

### 5. DATA

<br>