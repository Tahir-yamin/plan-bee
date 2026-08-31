"""
Schedule Comparison / Claim Digger Engine.
Compares two Primavera P6 XER files (e.g. Baseline vs Update) and produces
detailed variance reports on activities, logic ties, dates, durations, and costs.
"""

from typing import Dict, List, Any, Optional
from openplanco.parser.xer_parser import XERFile

class ScheduleComparator:
    def __init__(self, baseline_xer: XERFile, update_xer: XERFile):
        self.b_xer = baseline_xer
        self.u_xer = update_xer

    def compare(self) -> Dict[str, Any]:
        """Performs comprehensive schedule comparison."""
        b_tasks = {t.get("task_code"): t for t in (self.b_xer.task_table.records if self.b_xer.task_table else []) if t.get("task_code")}
        u_tasks = {t.get("task_code"): t for t in (self.u_xer.task_table.records if self.u_xer.task_table else []) if t.get("task_code")}

        added_codes = set(u_tasks.keys()) - set(b_tasks.keys())
        deleted_codes = set(b_tasks.keys()) - set(u_tasks.keys())
        common_codes = set(b_tasks.keys()) & set(u_tasks.keys())

        added_tasks = [u_tasks[c] for c in added_codes]
        deleted_tasks = [b_tasks[c] for c in deleted_codes]

        modified_tasks = []
        for code in common_codes:
            bt = b_tasks[code]
            ut = u_tasks[code]
            changes = {}

            # Duration changes
            b_dur = float(bt.get("target_durn_hr_cnt", 0) or 0) / 8.0
            u_dur = float(ut.get("target_durn_hr_cnt", 0) or 0) / 8.0
            if abs(b_dur - u_dur) > 0.01:
                changes["original_duration"] = {"baseline": b_dur, "update": u_dur, "diff": round(u_dur - b_dur, 2)}

            # Date changes
            for date_field in ["target_start_date", "target_end_date", "early_start_date", "early_end_date", "act_start_date", "act_end_date"]:
                b_val = bt.get(date_field, "")
                u_val = ut.get(date_field, "")
                if b_val != u_val and (b_val or u_val):
                    changes[date_field] = {"baseline": b_val, "update": u_val}

            # Float changes
            b_tf = float(bt.get("total_float_hr_cnt", 0) or 0) / 8.0
            u_tf = float(ut.get("total_float_hr_cnt", 0) or 0) / 8.0
            if abs(b_tf - u_tf) > 0.01:
                changes["total_float_days"] = {"baseline": b_tf, "update": u_tf, "variance": round(u_tf - b_tf, 2)}

            # Status change
            if bt.get("status_code") != ut.get("status_code"):
                changes["status"] = {"baseline": bt.get("status_code"), "update": ut.get("status_code")}

            if changes:
                modified_tasks.append({
                    "task_code": code,
                    "task_name": ut.get("task_name") or bt.get("task_name"),
                    "changes": changes
                })

        # Logic / Relationship differences
        rel_diff = self._compare_relationships()

        return {
            "summary": {
                "baseline_task_count": len(b_tasks),
                "update_task_count": len(u_tasks),
                "added_task_count": len(added_tasks),
                "deleted_task_count": len(deleted_tasks),
                "modified_task_count": len(modified_tasks),
                "added_relationships": len(rel_diff["added"]),
                "deleted_relationships": len(rel_diff["deleted"])
            },
            "added_tasks": added_tasks,
            "deleted_tasks": deleted_tasks,
            "modified_tasks": modified_tasks,
            "relationship_changes": rel_diff
        }

    def _compare_relationships(self) -> Dict[str, List[Any]]:
        b_id_map = {t.get("task_id"): t.get("task_code") for t in (self.b_xer.task_table.records if self.b_xer.task_table else [])}
        u_id_map = {t.get("task_id"): t.get("task_code") for t in (self.u_xer.task_table.records if self.u_xer.task_table else [])}

        def build_rel_set(xer: XERFile, id_map: Dict[str, str]):
            s = set()
            if not xer.pred_table:
                return s
            for p in xer.pred_table.records:
                succ_code = id_map.get(p.get("task_id"))
                pred_code = id_map.get(p.get("pred_task_id"))
                pred_type = p.get("pred_type", "PR_FS")
                lag = p.get("lag_hr_cnt", "0")
                if succ_code and pred_code:
                    s.add((pred_code, succ_code, pred_type, lag))
            return s

        b_rels = build_rel_set(self.b_xer, b_id_map)
        u_rels = build_rel_set(self.u_xer, u_id_map)

        added = [{"pred": r[0], "succ": r[1], "type": r[2], "lag": r[3]} for r in (u_rels - b_rels)]
        deleted = [{"pred": r[0], "succ": r[1], "type": r[2], "lag": r[3]} for r in (b_rels - u_rels)]

        return {"added": added, "deleted": deleted}
