https://github.com/DongilVision/DevOps/blob/main/README.md


* 클래스생성자는 파라메터를 가지지 않는다.
* 상태변수를 이용하여 최대한 외부제어를 간단히 한다.
* 스트링 포메팅

### 1. 자료형
* 인터페이스 선언
```C#
    public static Dictionary<string, TabItem> Tab 
        = new Dictionary<string, TabItem>();
    class PhotoList : List<Photo>
    {
    }
    class Photo{

    }
    public interface GraphBox {
        (int,int)   GetRange();
    }

    public enum Bound
    {
        MAX,
        MIN
    }
    
    public int max {
        get{}
        set{}
    }
```
* 객체조건
```C#
// State 필드
// 이벤트핸들러
public delegate void StateEventHandler(object sender, bool TChecked);
ublic event StateEventHandler StateChange;
Dispose();
Clone();
Save();
Load();
  
```
### 2. 레이아웃
### 컴포넌트
### 메뉴시스템
---
<details>
<summary>[예제] Key이베트 및 팝업메뉴</summary>

```C#
 box.KeyDown += (object sender, KeyEventArgs e) =>
            {

                if (e.Key == Key.D && Keyboard.Modifiers == ModifierKeys.Control)
                {
                    this.Duplicate();
                }
                if (e.Key == Key.X && Keyboard.Modifiers == ModifierKeys.Control)
                {
                    this.Dispose();
                }
                if (e.Key == Key.Delete)
                {
                    this.Dispose();
                }
            };
            ContextMenu contextmenu = new ContextMenu();
            box.ContextMenu = contextmenu;
            {
                MenuItem m1 = new MenuItem();
                m1.Header = "Duplicate";
                m1.InputGestureText = "Ctrl-D";
                m1.Click += (object sender, RoutedEventArgs e)=>{
                    UiConsole.WriteLine("노드를 복제합니다.");
                    this.Duplicate();
                };
                contextmenu.Items.Add(m1);
            }
            {
                MenuItem m2 = new MenuItem();
                m2.Header = "Delete";
                m2.InputGestureText = "Ctrl-X";
                m2.Click += (object sender, RoutedEventArgs e) => {
                    var title = String.Format("도구를 삭제할까요?");
                    if (MessageBox.Show(title, 
                    "Tool", MessageBoxButton.YesNo, MessageBoxImage.Warning) == MessageBoxResult.Yes)
                    {
                        this.Dispose();
                    }
                
                };
                contextmenu.Items.Add(m2);
            }
           
```
</details>

### 테이블
