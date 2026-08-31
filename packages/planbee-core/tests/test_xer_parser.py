import pytest
from planbee.parser.xer_parser import XERParser, XERFile
from planbee.parser.xer_writer import XERWriter
from planbee.analyzer.dcma_audit import DCMAAuditor
from planbee.network.cpm_optimizer import CPMOptimizer

SAMPLE_XER = """ERMHDR	20.12	1	EXPORT	PROJECT	PlanBee	Admin	Standard
%T	PROJECT
%F	proj_id	proj_short_name
%R	100	SAMPLE_PROJ
%T	TASK
%F	task_id	proj_id	task_code	task_name	task_type	status_code	target_durn_hr_cnt	remain_durn_hr_cnt	total_float_hr_cnt
%R	1	100	A1000	Mobilization	TT_Task	TK_NotStart	80.0	80.0	0.0
%R	2	100	A1010	Excavation	TT_Task	TK_NotStart	160.0	160.0	0.0
%R	3	100	A1020	Foundation	TT_Task	TK_NotStart	240.0	240.0	0.0
%T	TASKPRED
%F	task_pred_id	task_id	pred_task_id	pred_type	lag_hr_cnt
%R	501	2	1	PR_FS	0.0
%R	502	3	2	PR_FS	0.0
%R	503	3	1	PR_FS	0.0
%E
"""

def test_parse_and_write():
    xer = XERParser.parse_text(SAMPLE_XER)
    assert xer.task_table is not None
    assert len(xer.task_table.records) == 3
    assert xer.task_table.records[0]["task_code"] == "A1000"

    # Write and re-parse
    out_str = XERWriter.write_string(xer)
    re_parsed = XERParser.parse_text(out_str)
    assert len(re_parsed.task_table.records) == 3

def test_dcma_audit():
    xer = XERParser.parse_text(SAMPLE_XER)
    auditor = DCMAAuditor(xer)
    report = auditor.audit()
    assert "summary" in report
    assert "metrics" in report

def test_redundant_relationship_detection():
    xer = XERParser.parse_text(SAMPLE_XER)
    optimizer = CPMOptimizer(xer)
    redundant = optimizer.find_redundant_relationships()
    # In sample: 1->2 and 2->3, so 1->3 (task_pred_id 503) is redundant
    assert len(redundant) == 1
    assert redundant[0]["task_pred_id"] == "503"
