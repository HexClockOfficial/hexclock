Class MainWindow
    Dim allColors As New List(Of Color)
    Dim allSegments As New List(Of String) From {"SEG_A1", "SEG_A2", "SEG_B", "SEG_C", "SEG_D1", "SEG_D2", "SEG_E", "SEG_F", "SEG_G1", "SEG_G2", "SEG_H", "SEG_J", "SEG_K", "SEG_L", "SEG_M", "SEG_N"}

    Private Sub SEGMENTS_MouseDown(ByVal sender As System.Object, ByVal e As System.Windows.Input.MouseButtonEventArgs) Handles SEG_G1.MouseDown, SEG_N.MouseDown, SEG_M.MouseDown, SEG_L.MouseDown, SEG_G2.MouseDown, SEG_K.MouseDown, SEG_J.MouseDown, SEG_H.MouseDown, SEG_F.MouseDown, SEG_E.MouseDown, SEG_D1.MouseDown, SEG_D2.MouseDown, SEG_C.MouseDown, SEG_B.MouseDown, SEG_A2.MouseDown, SEG_A1.MouseDown
        If Mouse.LeftButton = MouseButtonState.Pressed Then
            Dim c As Color = colorPicker.GetColor()
            allColors(allSegments.IndexOf(sender.Name)) = c
            c.R *= 0.75
            c.G *= 0.75
            c.B *= 0.75
            c.R += 63
            c.G += 63
            c.B += 63
            sender.Fill = New SolidColorBrush(c)
        End If

        If Mouse.RightButton = MouseButtonState.Pressed Then
            Dim c As Color = allColors(allSegments.IndexOf(sender.Name))
            colorPicker.SetColor(c)
        End If
    End Sub

    Private Sub Window_Loaded(ByVal sender As System.Object, ByVal e As System.Windows.RoutedEventArgs) Handles MyBase.Loaded
        For i As Integer = 0 To 15
            allColors.Add(Color.FromRgb(0, 0, 0))
        Next
    End Sub

    Private Sub fillLabel_MouseDown(ByVal sender As System.Object, ByVal e As System.Windows.Input.MouseButtonEventArgs) Handles fillLabel.MouseDown
        Dim c As Color = colorPicker.GetColor()
        For i As Integer = 0 To 15
            allColors(i) = c
        Next
        c.R *= 0.75
        c.G *= 0.75
        c.B *= 0.75
        c.R += 63
        c.G += 63
        c.B += 63
        For Each p In {SEG_G1, SEG_N, SEG_M, SEG_L, SEG_G2, SEG_K, SEG_J, SEG_H, SEG_F, SEG_E, SEG_D1, SEG_D2, SEG_C, SEG_B, SEG_A2, SEG_A1}
            p.Fill = New SolidColorBrush(c)
        Next
    End Sub

    Private Sub clearLabel_MouseDown(ByVal sender As System.Object, ByVal e As System.Windows.Input.MouseButtonEventArgs) Handles clearLabel.MouseDown
        Dim c As Color = Color.FromRgb(0, 0, 0)
        For i As Integer = 0 To 15
            allColors(i) = c
        Next
        c.R *= 0.75
        c.G *= 0.75
        c.B *= 0.75
        c.R += 63
        c.G += 63
        c.B += 63
        For Each p In {SEG_G1, SEG_N, SEG_M, SEG_L, SEG_G2, SEG_K, SEG_J, SEG_H, SEG_F, SEG_E, SEG_D1, SEG_D2, SEG_C, SEG_B, SEG_A2, SEG_A1}
            p.Fill = New SolidColorBrush(c)
        Next
    End Sub

    Function UpdateCode() As String
        Dim CodeString As String = "["
        For Each c In allColors
            CodeString += "(0x" & c.R.ToString("X2") & ", 0x" & c.G.ToString("X2") & ", 0x" & c.B.ToString("X2") & "), "
        Next
        CodeString = CodeString.Substring(0, CodeString.Length - 2) & "]"
        Return CodeString
    End Function

    Private Sub codeLabel_MouseDown(ByVal sender As System.Object, ByVal e As System.Windows.Input.MouseButtonEventArgs) Handles codeLabel.MouseDown
        Clipboard.SetText(UpdateCode())
    End Sub

    Private Sub randomButton_MouseDown(ByVal sender As System.Object, ByVal e As System.Windows.Input.MouseButtonEventArgs) Handles randomButton.MouseDown
        Dim c As Color = Color.FromRgb(Rnd() * 255, Rnd() * 255, Rnd() * 255)
        colorPicker.SetColor(c)
    End Sub
End Class
