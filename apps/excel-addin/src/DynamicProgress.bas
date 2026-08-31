Attribute VB_Name = "DynamicProgress"
Option Explicit

Public Sub InsertEVMHeaders()
    Dim ws As Worksheet
    Set ws = ActiveSheet
    
    ws.Range("G1").Value = "Budget Total Cost (BAC)"
    ws.Range("H1").Value = "Planned Value (PV / BCWS)"
    ws.Range("I1").Value = "Earned Value (EV / BCWP)"
    ws.Range("J1").Value = "Actual Cost (AC / ACWP)"
    ws.Range("K1").Value = "Schedule Variance (SV)"
    ws.Range("L1").Value = "Cost Variance (CV)"
    ws.Range("M1").Value = "SPI"
    ws.Range("N1").Value = "CPI"
    
    ws.Range("G1:N1").Font.Bold = True
    ws.Range("G1:N1").Interior.Color = RGB(241, 245, 249)
    ws.Columns("G:N").AutoFit
End Sub
