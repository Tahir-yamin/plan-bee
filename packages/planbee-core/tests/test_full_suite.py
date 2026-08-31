import os
import pytest
from planbee.parser.xer_parser import XERParser, XERFile
from planbee.parser.xer_writer import XERWriter
from planbee.analyzer.dcma_audit import DCMAAuditor
from planbee.comparison.schedule_diff import ScheduleComparator
from planbee.network.cpm_optimizer import CPMOptimizer
from planbee.tia.forensic_tia import ForensicTIA
from planbee.converter.excel_xer import ExcelXERConverter

BASELINE_XER = """ERMHDR\t20.12\t1\tEXPORT\tPROJECT\tPlanBee\tAdmin\tStandard
%T\tPROJECT
%F\tproj_id\tproj_short_name
%R\t100\tPROJ_A
%T\tTASK
%F\ttask_id\tproj_id\ttask_code\ttask_name\ttask_type\tstatus_code\ttarget_durn_hr_cnt\tremain_durn_hr_cnt\ttotal_float_hr_cnt\tact_start_date\tact_end_date
%R\t1\t100\tACT-01\tDesign\tTT_Task\tTK_NotStart\t80.0\t80.0\t0.0\t\t
%R\t2\t100\tACT-02\tProcurement\tTT_Task\tTK_NotStart\t160.0\t160.0\t0.0\t\t
%R\t3\t100\tACT-03\tConstruction\tTT_Task\tTK_NotStart\t240.0\t240.0\t0.0\t\t
%T\tTASKPRED
%F\ttask_pred_id\ttask_id\tpred_task_id\tpred_type\tlag_hr_cnt
%R\t1\t2\t1\tPR_FS\t0.0
%R\t2\t3\t2\tPR_FS\t0.0
%E
"""

UPDATE_XER = """ERMHDR\t20.12\t1\tEXPORT\tPROJECT\tPlanBee\tAdmin\tStandard
%T\tPROJECT
%F\tproj_id\tproj_short_name
%R\t100\tPROJ_A
%T\tTASK
%F\ttask_id\tproj_id\ttask_code\ttask_name\ttask_type\tstatus_code\ttarget_durn_hr_cnt\tremain_durn_hr_cnt\ttotal_float_hr_cnt\tact_start_date\tact_end_date
%R\t1\t100\tACT-01\tDesign\tTT_Task\tTK_Complete\t80.0\t0.0\t0.0\t2026-01-01 08:00\t2026-01-10 17:00
%R\t2\t100\tACT-02\tProcurement\tTT_Task\tTK_Active\t160.0\t80.0\t-40.0\t2026-01-11 08:00\t
%R\t3\t100\tACT-03\tConstruction\tTT_Task\tTK_NotStart\t240.0\t240.0\t-40.0\t\t
%R\t4\t100\tACT-04\tCommissioning\tTT_Task\tTK_NotStart\t80.0\t80.0\t-40.0\t\t
%T\tTASKPRED
%F\ttask_pred_id\ttask_id\tpred_task_id\tpred_type\tlag_hr_cnt
%R\t1\t2\t1\tPR_FS\t0.0
%R\t2\t3\t2\tPR_FS\t0.0
%R\t3\t4\t3\tPR_FS\t0.0
%E
"""

def test_schedule_comparison():
    b_xer = XERParser.parse_text(BASELINE_XER)
    u_xer = XERParser.parse_text(UPDATE_XER)
    comp = ScheduleComparator(b_xer, u_xer)
    diff = comp.compare()

    assert diff["summary"]["baseline_task_count"] == 3
    assert diff["summary"]["update_task_count"] == 4
    assert diff["summary"]["added_task_count"] == 1
    assert diff["added_tasks"][0]["task_code"] == "ACT-04"
    assert diff["summary"]["modified_task_count"] >= 2

def test_forensic_tia():
    b_xer = XERParser.parse_text(BASELINE_XER)
    u_xer = XERParser.parse_text(UPDATE_XER)
    
    half_step = ForensicTIA.generate_half_step_schedule(b_xer, u_xer)
    zero_step = ForensicTIA.generate_zero_step_schedule(b_xer, u_xer)
    
    # Half-step should have updated progress on ACT-01
    act1_half = next(t for t in half_step.task_table.records if t["task_code"] == "ACT-01")
    assert act1_half["status_code"] == "TK_Complete"
    
    # Zero-step should have ACT-04 added but set to not started
    act4_zero = next(t for t in zero_step.task_table.records if t["task_code"] == "ACT-04")
    assert act4_zero["status_code"] == "TK_NotStart"

def test_cpm_zeroing():
    u_xer = XERParser.parse_text(UPDATE_XER)
    optimizer = CPMOptimizer(u_xer)
    zeroed = optimizer.zero_out_update()
    
    act1 = next(t for t in zeroed.task_table.records if t["task_code"] == "ACT-01")
    assert act1["status_code"] == "TK_NotStart"
    assert act1["act_start_date"] == ""
    assert act1["act_end_date"] == ""

def test_excel_converter(tmp_path):
    b_xer = XERParser.parse_text(BASELINE_XER)
    xlsx_path = str(tmp_path / "test_schedule.xlsx")
    ExcelXERConverter.xer_to_excel(b_xer, xlsx_path)
    assert os.path.exists(xlsx_path)
    
    reloaded_xer = ExcelXERConverter.excel_to_xer(xlsx_path)
    assert reloaded_xer.task_table is not None
    assert len(reloaded_xer.task_table.records) == 3
