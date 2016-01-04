Imports System.Net

Public Class EnterServerInfo
    Public ip_string As String = ""
    Public port As Integer = 0
    Public okay As Boolean = False

    Private Sub cancelButton_MouseDown(ByVal sender As System.Object, ByVal e As System.Windows.Input.MouseButtonEventArgs) Handles cancelButton.MouseDown
        Me.Close()
    End Sub

    Private Sub okayButton_MouseDown(ByVal sender As System.Object, ByVal e As System.Windows.Input.MouseButtonEventArgs) Handles okayButton.MouseDown
        If IsNumeric(portTextBox.Text) Then
            ip_string = ipTextBox.Text
            port = CInt(portTextBox.Text)
            okay = True
            Me.Close()
        Else
            MsgBox("Port must be numeric")
        End If
    End Sub

    Private Sub findLabel_MouseDown(ByVal sender As System.Object, ByVal e As System.Windows.Input.MouseButtonEventArgs) Handles findLabel.MouseDown
        Try
            Dim hostname As IPHostEntry = Dns.GetHostEntry("hexclock")
            Dim ip As IPAddress() = hostname.AddressList
            ipTextBox.Text = ip(0).ToString
        Catch ex As Exception
            MsgBox("Unable to find 'hexclock' host")
        End Try

    End Sub
End Class
