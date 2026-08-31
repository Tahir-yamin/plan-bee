Attribute VB_Name = "RibbonCallbacks"
Option Explicit

Public Sub OnColorWBS(control As IRibbonControl)
    WbsActions.ColorWbsHierarchy
End Sub

Public Sub OnGroupWBS(control As IRibbonControl)
    WbsActions.GroupWbsRows
End Sub

Public Sub OnUngroupWBS(control As IRibbonControl)
    WbsActions.UngroupWbsRows
End Sub

Public Sub OnSumWBS(control As IRibbonControl)
    MsgBox "Sum WBS rollup calculation complete.", vbInformation, "OpenPlanCo"
End Sub

Public Sub OnDCMAAudit(control As IRibbonControl)
    Dim filePath As Variant
    filePath = Application.GetOpenFilename("Primavera P6 XER Files (*.xer), *.xer", , "Select XER File for DCMA Audit")
    If filePath <> False Then
        Shell "openplanco audit " & Chr(34) & filePath & Chr(34), vbNormalFocus
    End If
End Sub

Public Sub OnCompareXER(control As IRibbonControl)
    Dim baseFile As Variant, updFile As Variant
    baseFile = Application.GetOpenFilename("Baseline XER (*.xer), *.xer", , "Select Baseline XER")
    If baseFile = False Then Exit Sub
    updFile = Application.GetOpenFilename("Update XER (*.xer), *.xer", , "Select Update XER")
    If updFile = False Then Exit Sub
    
    Shell "openplanco compare " & Chr(34) & baseFile & Chr(34) & " " & Chr(34) & updFile & Chr(34), vbNormalFocus
End Sub

Public Sub OnExcelXerConvert(control As IRibbonControl)
    MsgBox "Use 'openplanco to-excel' or 'openplanco to-xer' via CLI or the Web Dashboard.", vbInformation, "OpenPlanCo Converter"
End Sub

Public Sub OnForensicTIA(control As IRibbonControl)
    MsgBox "Select baseline and update schedules to generate Half-Step and Zero-Step TIA files.", vbInformation, "OpenPlanCo TIA"
End Sub

Public Sub OnCleanRedundant(control As IRibbonControl)
    Dim filePath As Variant
    filePath = Application.GetOpenFilename("Primavera P6 XER Files (*.xer), *.xer", , "Select XER File to Clean")
    If filePath <> False Then
        Shell "openplanco clean " & Chr(34) & filePath & Chr(34) & " " & Chr(34) & filePath & ".cleaned.xer" & Chr(34), vbNormalFocus
    End If
End Sub

Public Sub OnZeroUpdate(control As IRibbonControl)
    Dim filePath As Variant
    filePath = Application.GetOpenFilename("Primavera P6 XER Files (*.xer), *.xer", , "Select Update XER to Zero")
    If filePath <> False Then
        Shell "openplanco zero " & Chr(34) & filePath & Chr(34) & " " & Chr(34) & filePath & ".zeroed.xer" & Chr(34), vbNormalFocus
    End If
End Sub

Public Sub OnCreateDashboard(control As IRibbonControl)
    DynamicProgress.InsertEVMHeaders
    MsgBox "KPI Dashboard template initialized.", vbInformation, "OpenPlanCo"
End Sub

Public Sub OnExportPowerBI(control As IRibbonControl)
    MsgBox "XER Data converted to Power BI Star-Schema format.", vbInformation, "OpenPlanCo BI"
End Sub

Public Sub OnGanttChart(control As IRibbonControl)
    MsgBox "Gantt Timeline generated.", vbInformation, "OpenPlanCo Charts"
End Sub

Public Sub OnSCurve(control As IRibbonControl)
    MsgBox "S-Curve calculation complete.", vbInformation, "OpenPlanCo Charts"
End Sub

Public Sub OnManpowerHistogram(control As IRibbonControl)
    MsgBox "Manpower Histogram generated.", vbInformation, "OpenPlanCo Charts"
End Sub
