https://github.com/DongilVision/DevOps/blob/main/README.md

### 자료형

### 레이아웃
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
