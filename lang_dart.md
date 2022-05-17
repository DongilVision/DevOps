
### Key 설정방법
* <app dir>/android/app/build.gradle
* <app dir>/android/key.properties
*  https://flutter-ko.dev/docs/deployment/android
*  key는 android studio에서 만든다.

### 라이브러리 사용 및 권한
* pubspec.yaml (라이브러리등록)
 ```
 dependencies:
  flutter:
    sdk: flutter
  camera: 0.9.4+21
  http: 0.13.4
  connectivity: ^3.0.6
  flutter_beep: 1.0.0
  audioplayers: ^0.20.1
  flutter_blue: ^0.8.0
 ```
 ```
import 'package:flutter_beep/flutter_beep.dart';
import 'package:audioplayers/audioplayers.dart';
import 'package:flutter_blue/flutter_blue.dart';
 ```
* 
### Bundle 빌드

flutter clean
flutter build appbundle -release -debug



https://youtu.be/3Ck42C2ZCb8 (동영상 : Dart 기본)

# function parameter
* positional parameter
* optional parameter
* named parameter
* add ( { required int x, } ) { body }


arrow function
 ==> x+y+z
 
typedef operation = int Function(intx,int y)

https://youtu.be/mLQ-ehf3d6Y (플로터 기본 4가지) : 1강
4가지 위젯 : 글자, 이미지, 아이콘, 
  박스 : Container, SizedBox
  Center(
  child: Container( width:50~)
  
  
https://youtu.be/U6rLIFn59Kw 2강 레이어 control+space
* Scaffold (
    appBar: AppBar(),
    body: Container(),
    bottomNavigationBar: BottomAppBar(),
    ) // Scaffold
    Icons.phone, 
    Icons.message
    Icons.contact_page
    
 https://youtu.be/4KH4_6Gd6sE 3강
 
 https://youtu.be/ShmXbPpmIMU 4강 아파
