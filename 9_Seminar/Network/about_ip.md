* 컴퓨터 네트워크 주소체계

* MAC (Media Access Control address)
   * 형태 : "1f:23:33:55:f2:33" 
        * 총 48비트. 8비트씩 6자리. -> 2^48 = 281조
        * 앞 3자리는 '제조사 코드'
        * 뒤 3자리는 '기기 고유 코드' 
   * 이더넷 기반 기기에는 모두 다 하나씩 할당되어있다.(개당 1원)
   * 공장에서 생산될때 부여되는 물리 주소. 
   * MAC 변경
        * 과거 : ROM을 사용하여 변경이 불가능햇다.
        * 현재 : 플래시메모리 사용으로 변경이 가능하다. -> 이것을 이용한 해킹이 MAC 스푸핑이다.
* IP (Internet Protocol)
    * IPv4 
        * 형태 : 192.168.2.1
        * 32비트 -> 2^35 = 43억개 -> 갯수 부족 -> 라우터를 이용하여 해결
    * IPv6 
        * 형태 : 2606:2800:0220:0001:0248:1893:25c8:1946
        * 128비트 -> 2^128 = 3.4 * 10^38 -> 너무 많음. 걱정이 없음. IPv4에서 넘어가는중이다.
    * 공인 IP
        * IPv4 기준으로 1.0.0.0 ~ 223.255.255.255 가 이에 해당한다. 지역별로 쓸 수 있는 IP의 주소의 범위가 있으며, 기관을 통해 사용권을 요청하여 할당받아 사용해야한다.
    * 사설 IP
        * 부족한 IPv4를 효과적으로 사용할 수 있는 방법이다. 
    * ping , ifconfig 통하여 관리함.
    * 동적으로 DHCP를 통하여 부여되거나(자동 IP), PC에서 정적으로 줄수 있음(수동 IP).
    * PC에서 정적으로 설정할때는 아래를 같이 설정해야 한다.
        * NetMask : 192.158.2.255 / C클래스 / 
            * IP주소가 어느 네트워크에 속하는지 판단하는데 사용.
            * 일반적인 형식 : 255.255.255.0(10진수), 11111111.11111111.11111111.00000000(2진수)
            * ex. IP : 192.168.1.50, NetMask : 255.255.255.0 => ip 주소 : 192.168.1, 호스트 : 50
        * Gateway :  192.168.2.1 / 넷마스크가 다를 경우 , 나가는 문,  공유기의 IP 주소를 가르킴
        * DNS : url --> ip 변화기의 주소.
* URL 
    * DNS (Domain Naming Server) 에 등록된 주소, www.chosun.com
    * DNS를 관리하는 기관에 의뢰하여 유료로 등록할 수 있다.
    * nslookup을 통하여 확인가능
        * Window : Resolve-DnsName
        * Linux / MacOS : dig

* routetrace
* arp 

# C# 에서 IP 읽어오는 법

## 1. xaml에서 ip를 출력 시킬 곳에 Binding을 합니다.

```xml
<Window
    Title = "{Binding MainWindowTitle}">
</Window>
```

* 위의 예제는 Title에 적용하여 wpf실행시 창에 출력되도록 만들었습니다.

## 2. IP를 구하는 메소드 & 인터페이스 구현

```cs
 private string GetLocalIPAddress() {
            // IP 주소를 가져오는 방법은 다양하지만, 간단하게 Dns 클래스를 사용합니다.
            string hostName = Dns.GetHostName();
            IPHostEntry hostEntry = Dns.GetHostEntry(hostName);
            IPAddress ipAddress = hostEntry.AddressList.FirstOrDefault(ip => ip.AddressFamily == System.Net.Sockets.AddressFamily.InterNetwork);
            return ipAddress?.ToString() ?? "Unknown";
        }

        // INotifyPropertyChanged 인터페이스 구현
        public event PropertyChangedEventHandler PropertyChanged;
        private void OnPropertyChanged([CallerMemberName] string propertyName = null) {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }
```

## 3. Title에 IP 추가시키기

```cs
 public MainWindow() {
            InitializeComponent();
            DataContext = this;

            // 자신의 IP 주소를 가져와서 Title에 추가합니다.
            string ipAddress = GetLocalIPAddress();
            MainWindowTitle = "TCP TESTER - " + ipAddress;
        }
```

+ 함수를 호출하여 IP를 ipAddress 변수에 저장합니다.
+ 바인딩을 통하여 Title에 IP를 출력합니다.

