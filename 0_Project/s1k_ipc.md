## IPC 포멧
### Identifier (5Byte) - 인식자, Packet ID (page 8)

+ Identifier(5Bytes) = Start of Packet(2Bytes) + 송신 Device ID(1Bytes) + 수신 Device ID(1Bytes) + Handshake(1Bytes)
   

| Start of Packet | 송신 Device | 수신 Device | Handshake |
|-|-|-|-|
| 2 Bytes | 1 Bytes |  1 Bytes |  1 Bytes | 
| [0xFFFF] | pc : [0x00]<br> smart Camera : [0x01] ~ [0xFE] |  pc : [0x00]<br> smart Camera : [0x01] ~ [0xFE] |  [0xFF]<br> Response : ACK(0x00), NACK(0x01), Command SKIP(0x02) | 

<br>

### MainCode(1Byte) - 주 색인
+ [0x01](page 12) : Interface Configure (인터페이스 구성) 
+ [0x02](page 19) : Platform Version
+ [0x03](page 22) : Image Frame Configure (이미지 프레임 구성)
+ [0x04](page 29) : Illumination Controller Configure (조명 컨트롤러 구성)
+ [0x05](page 30) : I/O
+ [0x06](page 34) : File Management
+ [0x07](page 48) : File Transfer PtoS
+ [0x08](page 49) : File Transfer StoP
+ [0x09](page 50) : Operation Result
+ [0x0A](page 52) : Operation Result