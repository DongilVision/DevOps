
### Combo 사용법

### DataGrid
* C# 화일에서 ENUM과 ItemClass를 정의한다.
```
public enum StatusEnum
    {
        등록 = 1,
        진행,
        완료
    }

public class DataItem {
    public StatusEnum Status { get; set;}
    --- 중략--
    }
```
* XAML 화일에서 DataProvider 와 
```
xmlns:core="clr-namespace:System;assembly=mscorlib"
<UserControl.Resources>
    <ObjectDataProvider x:Key="myEnum" 
                MethodName="GetValues" 
                ObjectType="{x:Type core:Enum}">
        <ObjectDataProvider.MethodParameters>
            <x:Type Type="local:StatusEnum"/>
        </ObjectDataProvider.MethodParameters>
    </ObjectDataProvider>
</UserControl.Resources>

<DataGridComboBoxColumn Header="Order Status"  
    SelectedItemBinding="{Binding Status}" 
    ItemsSource="{Binding Source={StaticResource myEnum}}" />
```

```
 <DataGridTemplateColumn Width="300">
    <DataGridTemplateColumn.CellTemplate>
        <DataTemplate>
            <ComboBox HorizontalContentAlignment="Center">
                <ComboBox.Items>
                    <sys:String>string1</sys:String>
                    <sys:String>string2</sys:String>
                    <sys:String>string3</sys:String>                                
                </ComboBox.Items>
            </ComboBox>
        </DataTemplate>
    </DataGridTemplateColumn.CellTemplate>
</DataGridTemplateColumn>                       
```