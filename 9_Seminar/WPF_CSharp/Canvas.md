
* Canvas 객체에서 스케일을 가져오는 방법
```C#
public static ScaleTransform GetScaleTransform(Canvas canvas)
{
    TransformGroup tg = (TransformGroup)(canvas.RenderTransform);
    foreach (var st in tg.Children)
    {
        if (st.GetType() == typeof(ScaleTransform))
        {
            ScaleTransform scaleTransform = (ScaleTransform)st;
            return scaleTransform;
        }
    }
    return null;
}
```
