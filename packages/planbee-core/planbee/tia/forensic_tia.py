"""
Forensic Time Impact Analysis (TIA) Engine.
Generates Half-Step (progress only) and Zero-Step (logic changes only) XER schedules
to isolate contractor vs employer delays.
"""

from typing import Tuple
import copy
from planbee.parser.xer_parser import XERFile

class ForensicTIA:
    @staticmethod
    def generate_half_step_schedule(previous_xer: XERFile, current_xer: XERFile) -> XERFile:
        """
        Creates a Half-Step Schedule:
        Keeps previous schedule's logic ties and calendars, but applies current schedule's progress
        (actual dates, remaining durations, percent completes).
        """
        half_step = copy.deepcopy(previous_xer)
        
        curr_tasks = {t.get("task_code"): t for t in (current_xer.task_table.records if current_xer.task_table else []) if t.get("task_code")}
        
        if half_step.task_table:
            for t in half_step.task_table.records:
                code = t.get("task_code")
                if code in curr_tasks:
                    ct = curr_tasks[code]
                    t["status_code"] = ct.get("status_code", t.get("status_code"))
                    t["act_start_date"] = ct.get("act_start_date", "")
                    t["act_end_date"] = ct.get("act_end_date", "")
                    t["remain_durn_hr_cnt"] = ct.get("remain_durn_hr_cnt", t.get("remain_durn_hr_cnt"))
                    t["phys_complete_pct"] = ct.get("phys_complete_pct", t.get("phys_complete_pct"))
                    
        return half_step

    @staticmethod
    def generate_zero_step_schedule(previous_xer: XERFile, current_xer: XERFile) -> XERFile:
        """
        Creates a Zero-Step Schedule:
        Keeps previous schedule's progress/status, but incorporates all new logic changes,
        added activities, and scope revisions from the current schedule.
        """
        zero_step = copy.deepcopy(current_xer)
        prev_tasks = {t.get("task_code"): t for t in (previous_xer.task_table.records if previous_xer.task_table else []) if t.get("task_code")}

        if zero_step.task_table:
            for t in zero_step.task_table.records:
                code = t.get("task_code")
                if code in prev_tasks:
                    pt = prev_tasks[code]
                    t["status_code"] = pt.get("status_code", "TK_NotStart")
                    t["act_start_date"] = pt.get("act_start_date", "")
                    t["act_end_date"] = pt.get("act_end_date", "")
                    t["remain_durn_hr_cnt"] = pt.get("remain_durn_hr_cnt", t.get("target_durn_hr_cnt"))
                    t["phys_complete_pct"] = pt.get("phys_complete_pct", "0")
                else:
                    # New task added: set as not started
                    t["status_code"] = "TK_NotStart"
                    t["act_start_date"] = ""
                    t["act_end_date"] = ""
                    t["phys_complete_pct"] = "0"
                    t["remain_durn_hr_cnt"] = t.get("target_durn_hr_cnt", "0")

        return zero_step
