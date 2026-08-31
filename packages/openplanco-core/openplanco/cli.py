"""
Command-Line Interface (CLI) for OpenPlanCo.
Usage:
    openplanco audit <file.xer> [--output json/text]
    openplanco compare <baseline.xer> <update.xer>
    openplanco clean <input.xer> <output.xer>
    openplanco zero <input.xer> <output.xer>
    openplanco to-excel <input.xer> <output.xlsx>
    openplanco to-xer <input.xlsx> <output.xer>
    openplanco tia --prev <prev.xer> --curr <curr.xer> --out-half <half.xer> --out-zero <zero.xer>
"""

import argparse
import sys
import json
from openplanco.parser.xer_parser import XERParser
from openplanco.parser.xer_writer import XERWriter
from openplanco.analyzer.dcma_audit import DCMAAuditor
from openplanco.comparison.schedule_diff import ScheduleComparator
from openplanco.network.cpm_optimizer import CPMOptimizer
from openplanco.tia.forensic_tia import ForensicTIA
from openplanco.converter.excel_xer import ExcelXERConverter

def main():
    parser = argparse.ArgumentParser(
        prog="openplanco",
        description="OpenPlanCo - Modern Primavera P6 & Project Controls Toolkit"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Audit command
    p_audit = subparsers.add_parser("audit", help="Run DCMA 14-Point Health Audit on an XER file")
    p_audit.add_argument("file", help="Path to .xer file")
    p_audit.add_argument("--json", action="store_true", help="Output results as JSON")

    # Compare command
    p_compare = subparsers.add_parser("compare", help="Compare Baseline vs Update XER files")
    p_compare.add_argument("baseline", help="Baseline .xer file")
    p_compare.add_argument("update", help="Update .xer file")
    p_compare.add_argument("--json", action="store_true", help="Output results as JSON")

    # Clean command
    p_clean = subparsers.add_parser("clean", help="Remove redundant logic ties from an XER file")
    p_clean.add_argument("input", help="Input .xer file")
    p_clean.add_argument("output", help="Output cleaned .xer file")

    # Zero command
    p_zero = subparsers.add_parser("zero", help="Zero-out actuals to create a baseline from an update XER")
    p_zero.add_argument("input", help="Input .xer file")
    p_zero.add_argument("output", help="Output zeroed .xer file")

    # Excel export
    p_to_excel = subparsers.add_parser("to-excel", help="Convert XER file to multi-tab Excel workbook")
    p_to_excel.add_argument("input", help="Input .xer file")
    p_to_excel.add_argument("output", help="Output .xlsx file")

    # XER export
    p_to_xer = subparsers.add_parser("to-xer", help="Convert Excel workbook to XER file")
    p_to_xer.add_argument("input", help="Input .xlsx file")
    p_to_xer.add_argument("output", help="Output .xer file")

    # TIA command
    p_tia = subparsers.add_parser("tia", help="Generate TIA Half-Step and Zero-Step forensic schedules")
    p_tia.add_argument("--prev", required=True, help="Previous update .xer")
    p_tia.add_argument("--curr", required=True, help="Current update .xer")
    p_tia.add_argument("--out-half", required=True, help="Output half-step .xer")
    p_tia.add_argument("--out-zero", required=True, help="Output zero-step .xer")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "audit":
        xer = XERParser.parse_file(args.file)
        auditor = DCMAAuditor(xer)
        res = auditor.audit()
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            print(f"\n=======================================================")
            print(f"       DCMA 14-POINT SCHEDULE ASSESSMENT REPORT       ")
            print(f"=======================================================")
            print(f"Overall Health Score: {res['summary']['health_score_pct']}% ({res['summary']['passed_checks']}/{res['summary']['total_checks']} Passed)\n")
            for k, v in res["metrics"].items():
                status_symbol = "[PASS]" if "PASS" in v["status"] else "[FAIL]"
                print(f"{status_symbol:8} {v['name']:<50} | Actual: {v.get('actual_pct', v.get('actual_val', 'N/A'))}% (Target: {v.get('threshold', 'N/A')})")

    elif args.command == "compare":
        b_xer = XERParser.parse_file(args.baseline)
        u_xer = XERParser.parse_file(args.update)
        comp = ScheduleComparator(b_xer, u_xer)
        diff = comp.compare()
        if args.json:
            print(json.dumps(diff, indent=2))
        else:
            print(f"\n=======================================================")
            print(f"              SCHEDULE COMPARISON REPORT              ")
            print(f"=======================================================")
            print(f"Baseline Activities : {diff['summary']['baseline_task_count']}")
            print(f"Update Activities   : {diff['summary']['update_task_count']}")
            print(f"Added Activities    : {diff['summary']['added_task_count']}")
            print(f"Deleted Activities  : {diff['summary']['deleted_task_count']}")
            print(f"Modified Activities : {diff['summary']['modified_task_count']}")
            print(f"Added Relationships : {diff['summary']['added_relationships']}")
            print(f"Deleted Relationships: {diff['summary']['deleted_relationships']}")

    elif args.command == "clean":
        xer = XERParser.parse_file(args.input)
        optimizer = CPMOptimizer(xer)
        cleaned_xer, count = optimizer.remove_redundant_relationships()
        XERWriter.write_file(cleaned_xer, args.output)
        print(f"Cleaned {count} redundant relationship(s). Output written to: {args.output}")

    elif args.command == "zero":
        xer = XERParser.parse_file(args.input)
        optimizer = CPMOptimizer(xer)
        zeroed_xer = optimizer.zero_out_update()
        XERWriter.write_file(zeroed_xer, args.output)
        print(f"Successfully created baseline-style zeroed XER at: {args.output}")

    elif args.command == "to-excel":
        xer = XERParser.parse_file(args.input)
        ExcelXERConverter.xer_to_excel(xer, args.output)
        print(f"Exported XER to Excel: {args.output}")

    elif args.command == "to-xer":
        xer = ExcelXERConverter.excel_to_xer(args.input)
        XERWriter.write_file(xer, args.output)
        print(f"Exported Excel to XER: {args.output}")

    elif args.command == "tia":
        p_xer = XERParser.parse_file(args.prev)
        c_xer = XERParser.parse_file(args.curr)
        half_xer = ForensicTIA.generate_half_step_schedule(p_xer, c_xer)
        zero_xer = ForensicTIA.generate_zero_step_schedule(p_xer, c_xer)
        XERWriter.write_file(half_xer, args.out_half)
        XERWriter.write_file(zero_xer, args.out_zero)
        print(f"Generated Half-Step Schedule: {args.out_half}")
        print(f"Generated Zero-Step Schedule: {args.out_zero}")

if __name__ == "__main__":
    main()
