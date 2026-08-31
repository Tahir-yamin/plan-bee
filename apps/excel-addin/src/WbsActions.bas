Attribute VB_Name = "WbsActions"
Option Explicit

Public Function GetWbsColor(level As Long) As Long
    Select Case level
        Case 1: GetWbsColor = RGB(30, 41, 59)
        Case 2: GetWbsColor = RGB(51, 65, 85)
        Case 3: GetWbsColor = RGB(71, 85, 105)
        Case 4: GetWbsColor = RGB(100, 116, 139)
        Case 5: GetWbsColor = RGB(148, 163, 184)
        Case Else: GetWbsColor = RGB(226, 232, 240)
    End Select
End Function

Public Sub ColorWbsHierarchy()
    Dim ws As Worksheet
    Dim lastRow As Long, r As Long
    Dim wbsLevel As Long
    Dim cellVal As String
    
    Set ws = ActiveSheet
    lastRow = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row
    If lastRow < 2 Then Exit Sub
    
    Application.ScreenUpdating = False
    
    For r = 2 To lastRow
        cellVal = Trim(CStr(ws.Cells(r, 1).Value))
        If cellVal <> "" Then
            wbsLevel = UBound(Split(cellVal, ".")) + 1
            If wbsLevel > 0 And wbsLevel <= 5 Then
                With ws.Range(ws.Cells(r, 1), ws.Cells(r, 20))
                    .Interior.Color = GetWbsColor(wbsLevel)
                    If wbsLevel <= 3 Then
                        .Font.Color = RGB(255, 255, 255)
                        .Font.Bold = True
                    Else
                        .Font.Color = RGB(15, 23, 42)
                        .Font.Bold = True
                    End If
                End With
            End If
        End If
    Next r
    
    Application.ScreenUpdating = True
    MsgBox "WBS coloring applied successfully!", vbInformation, "PlanBee"
End Sub

Public Sub GroupWbsRows()
    Dim ws As Worksheet
    Dim lastRow As Long, r As Long
    Dim wbsLevel As Long
    Dim cellVal As String
    
    Set ws = ActiveSheet
    lastRow = ws.Cells(ws.Rows.Count, 1).End(xlUp).Row
    If lastRow < 2 Then Exit Sub
    
    On Error Resume Next
    ws.Cells.ClearOutline
    On Error GoTo 0
    
    Application.ScreenUpdating = False
    For r = 2 To lastRow
        cellVal = Trim(CStr(ws.Cells(r, 1).Value))
        If cellVal <> "" Then
            wbsLevel = UBound(Split(cellVal, ".")) + 1
            If wbsLevel > 1 Then
                ws.Rows(r).OutlineLevel = wbsLevel
            End If
        End If
    Next r
    
    ws.Outline.ShowLevels RowLevels:=2
    Application.ScreenUpdating = True
    MsgBox "WBS grouping created successfully!", vbInformation, "PlanBee"
End Sub

Public Sub UngroupWbsRows()
    Dim ws As Worksheet
    Set ws = ActiveSheet
    On Error Resume Next
    ws.Cells.ClearOutline
    On Error GoTo 0
    MsgBox "WBS outlines cleared.", vbInformation, "PlanBee"
End Sub
