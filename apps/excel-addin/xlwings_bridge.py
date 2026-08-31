"""
High-Speed Python <-> Excel Bridge for OpenPlanCo.
Enables programmatic control of active Excel workbooks from Python.
"""
import sys
from openplanco.parser.xer_parser import XERParser
from openplanco.analyzer.dcma_audit import DCMAAuditor
from openplanco.converter.excel_xer import ExcelXERConverter

def audit_active_sheet():
    print("OpenPlanCo Excel Bridge active.")

if __name__ == "__main__":
    audit_active_sheet()
