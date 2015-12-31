Public Class COLORPICKER
    Class HSV
        Public H As Decimal
        Public S As Decimal
        Public V As Decimal
        Sub New(ByVal h As Decimal, ByVal s As Decimal, ByVal v As Decimal)
            Me.H = h
            Me.S = s
            Me.V = v
        End Sub
    End Class

    Class RGB
        Public R As Decimal
        Public G As Decimal
        Public B As Decimal
        Sub New(ByVal r As Decimal, ByVal g As Decimal, ByVal b As Decimal)
            Me.R = r
            Me.G = g
            Me.B = b
        End Sub
    End Class

    Dim mainHSV As New HSV(340, 80, 60)

    Private Sub Canvas1_MouseMove(ByVal sender As System.Object, ByVal e As System.Windows.Input.MouseEventArgs) Handles Canvas1.MouseMove
        If Mouse.LeftButton = MouseButtonState.Pressed Then
            mainHSV.S = 100 - Math.Max(Math.Min(((Mouse.GetPosition(Canvas1).Y - 10) / (Canvas1.ActualHeight - 20)), 1), 0) * 100
            updatePicker()
        End If

        If Mouse.RightButton = MouseButtonState.Pressed Then
            mainHSV.V = 100 - Math.Max(Math.Min(((Mouse.GetPosition(Canvas1).Y - 10) / (Canvas1.ActualHeight - 20)), 1), 0) * 100
            updatePicker()
        End If
    End Sub

    Private Sub Canvas1_MouseDown(ByVal sender As System.Object, ByVal e As System.Windows.Input.MouseButtonEventArgs) Handles Canvas1.MouseDown
        If Mouse.MiddleButton = MouseButtonState.Pressed Then
            Try
                Dim clip_color As Color = ColorConverter.ConvertFromString(Clipboard.GetText.Replace(" ", ""))
                Dim hsv = RGBtoHSV(New RGB(clip_color.R, clip_color.G, clip_color.B))
                mainHSV = hsv
                updatePicker()
                COLORLABEL.Content = "#" & clip_color.R.ToString("X2") & clip_color.G.ToString("X2") & clip_color.B.ToString("X2")
            Catch ex As Exception

            End Try
        Else
            Canvas1_MouseMove(Nothing, Nothing)
        End If
    End Sub

    Private Sub Canvas1_MouseWheel(ByVal sender As System.Object, ByVal e As System.Windows.Input.MouseWheelEventArgs) Handles Canvas1.MouseWheel
        mainHSV.H += e.Delta / 60
        If mainHSV.H < 0 Then mainHSV.H += 360
        mainHSV.H = mainHSV.H Mod 360
        updatePicker()
    End Sub


    Sub updatePicker()
        Dim rgb = HSVtoRGB(mainHSV)
        Canvas1.Background = New SolidColorBrush(Color.FromRgb(rgb.R, rgb.G, rgb.B))

        saturationBar.Height = 20
        saturationBar.Width = Canvas1.ActualWidth / 2
        Canvas.SetLeft(saturationBar, 0)
        Canvas.SetBottom(saturationBar, (Canvas1.ActualHeight - 20) * (mainHSV.S / 100.0))

        brightnessBar.Height = 20
        brightnessBar.Width = Canvas1.ActualWidth / 2
        Canvas.SetRight(brightnessBar, 0)
        Canvas.SetBottom(brightnessBar, (Canvas1.ActualHeight - 20) * (mainHSV.V / 100.0))

        COLORLABEL.Content = "#" & CInt(rgb.R).ToString("X2") & CInt(rgb.G).ToString("X2") & CInt(rgb.B).ToString("X2")
    End Sub

    Public Function RGBtoHSV(ByVal rgb As RGB) As HSV
        ''# Normalize the RGB values by scaling them to be between 0 and 1
        Dim red As Decimal = rgb.R / 255D
        Dim green As Decimal = rgb.G / 255D
        Dim blue As Decimal = rgb.B / 255D

        Dim minValue As Decimal = Math.Min(red, Math.Min(green, blue))
        Dim maxValue As Decimal = Math.Max(red, Math.Max(green, blue))
        Dim delta As Decimal = maxValue - minValue

        Dim h As Decimal
        Dim s As Decimal
        Dim v As Decimal = maxValue

        ''# Calculate the hue (in degrees of a circle, between 0 and 360)
        Select Case maxValue
            Case red
                If green >= blue Then
                    If delta = 0 Then
                        h = 0
                    Else
                        h = 60 * (green - blue) / delta
                    End If
                ElseIf green < blue Then
                    h = 60 * (green - blue) / delta + 360
                End If
            Case green
                h = 60 * (blue - red) / delta + 120
            Case blue
                h = 60 * (red - green) / delta + 240
        End Select

        ''# Calculate the saturation (between 0 and 1)
        If maxValue = 0 Then
            s = 0
        Else
            s = 1D - (minValue / maxValue)
        End If

        ''# Scale the saturation and value to a percentage between 0 and 100
        s *= 100
        v *= 100

        ''# Return a color in the new color space
        Return New HSV(CInt(Math.Round(h, MidpointRounding.AwayFromZero)), _
                       CInt(Math.Round(s, MidpointRounding.AwayFromZero)), _
                       CInt(Math.Round(v, MidpointRounding.AwayFromZero)))
    End Function

    Public Function HSVtoRGB(ByVal hsv As HSV) As RGB
        ''# Scale the Saturation and Value components to be between 0 and 1
        Dim hue As Decimal = hsv.H
        Dim sat As Decimal = hsv.S / 100D
        Dim val As Decimal = hsv.V / 100D

        Dim r As Decimal
        Dim g As Decimal
        Dim b As Decimal

        If sat = 0 Then
            ''# If the saturation is 0, then all colors are the same.
            ''# (This is some flavor of gray.)
            r = val
            g = val
            b = val
        Else
            ''# Calculate the appropriate sector of a 6-part color wheel
            Dim sectorPos As Decimal = hue / 60D
            Dim sectorNumber As Integer = CInt(Math.Floor(sectorPos))

            ''# Get the fractional part of the sector
            ''# (that is, how many degrees into the sector you are)
            Dim fractionalSector As Decimal = sectorPos - sectorNumber

            ''# Calculate values for the three axes of the color
            Dim p As Decimal = val * (1 - sat)
            Dim q As Decimal = val * (1 - (sat * fractionalSector))
            Dim t As Decimal = val * (1 - (sat * (1 - fractionalSector)))

            ''# Assign the fractional colors to red, green, and blue
            ''# components based on the sector the angle is in
            Select Case sectorNumber
                Case 0, 6
                    r = val
                    g = t
                    b = p
                Case 1
                    r = q
                    g = val
                    b = p
                Case 2
                    r = p
                    g = val
                    b = t
                Case 3
                    r = p
                    g = q
                    b = val
                Case 4
                    r = t
                    g = p
                    b = val
                Case 5
                    r = val
                    g = p
                    b = q
            End Select
        End If

        ''# Scale the red, green, and blue values to be between 0 and 255
        r *= 255
        g *= 255
        b *= 255

        ''# Return a color in the new color space
        Return New RGB(CInt(Math.Round(r, MidpointRounding.AwayFromZero)), _
                       CInt(Math.Round(g, MidpointRounding.AwayFromZero)), _
                       CInt(Math.Round(b, MidpointRounding.AwayFromZero)))
    End Function

    Private Sub UserControl_Loaded(ByVal sender As System.Object, ByVal e As System.Windows.RoutedEventArgs) Handles MyBase.Loaded
        updatePicker()
    End Sub

    Private Sub UserControl_SizeChanged(ByVal sender As System.Object, ByVal e As System.Windows.SizeChangedEventArgs) Handles MyBase.SizeChanged
        updatePicker()
    End Sub

    Public Function GetColor() As Color
        Dim rgb = HSVtoRGB(mainHSV)
        Return Color.FromRgb(rgb.R, rgb.G, rgb.B)
    End Function

    Public Sub SetColor(ByVal rgb As Color)
        Dim hsv = RGBtoHSV(New RGB(rgb.R, rgb.G, rgb.B))
        mainHSV = hsv
        updatePicker()
    End Sub

End Class