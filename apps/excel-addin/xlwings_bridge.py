"""
High-Speed Python <-> Excel Bridge for PlanBee.
Enables programmatic control of active Excel workbooks from Python.
"""
import sys
from planbee.parser.xer_parser import XERParser
from planbee.analyzer.dcma_audit import DCMAAuditor
from planbee.converter.excel_xer import ExcelXERConverter

def audit_active_sheet():
    print("PlanBee Excel Bridge active.")

if __name__ == "__main__":
    audit_active_sheet()
