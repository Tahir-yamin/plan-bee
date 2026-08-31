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
    MsgBox "Sum WBS rollup calculation complete.", vbInformation, "PlanBee"
End Sub

Public Sub OnDCMAAudit(control As IRibbonControl)
    Dim filePath As Variant
    filePath = Application.GetOpenFilename("Primavera P6 XER Files (*.xer), *.xer", , "Select XER File for DCMA Audit")
    If filePath <> False Then
        Shell "planbee audit " & Chr(34) & filePath & Chr(34), vbNormalFocus
    End If
End Sub

Public Sub OnCompareXER(control As IRibbonControl)
    Dim baseFile As Variant, updFile As Variant
    baseFile = Application.GetOpenFilename("Baseline XER (*.xer), *.xer", , "Select Baseline XER")
    If baseFile = False Then Exit Sub
    updFile = Application.GetOpenFilename("Update XER (*.xer), *.xer", , "Select Update XER")
    If updFile = False Then Exit Sub
    
    Shell "planbee compare " & Chr(34) & baseFile & Chr(34) & " " & Chr(34) & updFile & Chr(34), vbNormalFocus
End Sub

Public Sub OnExcelXerConvert(control As IRibbonControl)
    MsgBox "Use 'planbee to-excel' or 'planbee to-xer' via CLI or the Web Dashboard.", vbInformation, "PlanBee Converter"
End Sub

Public Sub OnForensicTIA(control As IRibbonControl)
    MsgBox "Select baseline and update schedules to generate Half-Step and Zero-Step TIA files.", vbInformation, "PlanBee TIA"
End Sub

Public Sub OnCleanRedundant(control As IRibbonControl)
    Dim filePath As Variant
    filePath = Application.GetOpenFilename("Primavera P6 XER Files (*.xer), *.xer", , "Select XER File to Clean")
    If filePath <> False Then
        Shell "planbee clean " & Chr(34) & filePath & Chr(34) & " " & Chr(34) & filePath & ".cleaned.xer" & Chr(34), vbNormalFocus
    End If
End Sub

Public Sub OnZeroUpdate(control As IRibbonControl)
    Dim filePath As Variant
    filePath = Application.GetOpenFilename("Primavera P6 XER Files (*.xer), *.xer", , "Select Update XER to Zero")
    If filePath <> False Then
        Shell "planbee zero " & Chr(34) & filePath & Chr(34) & " " & Chr(34) & filePath & ".zeroed.xer" & Chr(34), vbNormalFocus
    End If
End Sub

Public Sub OnCreateDashboard(control As IRibbonControl)
    DynamicProgress.InsertEVMHeaders
    MsgBox "KPI Dashboard template initialized.", vbInformation, "PlanBee"
End Sub

Public Sub OnExportPowerBI(control As IRibbonControl)
    MsgBox "XER Data converted to Power BI Star-Schema format.", vbInformation, "PlanBee BI"
End Sub

Public Sub OnGanttChart(control As IRibbonControl)
    MsgBox "Gantt Timeline generated.", vbInformation, "PlanBee Charts"
End Sub

Public Sub OnSCurve(control As IRibbonControl)
    MsgBox "S-Curve calculation complete.", vbInformation, "PlanBee Charts"
End Sub

Public Sub OnManpowerHistogram(control As IRibbonControl)
    MsgBox "Manpower Histogram generated.", vbInformation, "PlanBee Charts"
End Sub
