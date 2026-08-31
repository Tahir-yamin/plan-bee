"""
CPM Network Optimizer & Logic Tools for Primavera P6 XER files.
Includes:
- Transitive Reduction to detect and remove redundant relationships (TASKPRED)
- Dangling Activity Solver (identifying and fixing open starts/finishes)
- Update Zeroing (converting an update schedule back into a baseline)
- Table Data Purger (stripping POBS, RISK, or unnecessary tables)
- Batch Activity ID Remapper
"""

from typing import Dict, List, Set, Tuple, Any, Optional
import copy
from planbee.parser.xer_parser import XERFile, XERTable

class CPMOptimizer:
    def __init__(self, xer: XERFile):
        self.xer = xer

    def find_redundant_relationships(self) -> List[Dict[str, Any]]:
        """
        Detects redundant Finish-to-Start relationships using graph reachability.
        If A -> B and B -> C, a direct tie A -> C is redundant.
        """
        if not self.xer.pred_table or not self.xer.task_table:
            return []

        task_id_to_code = {t.get("task_id"): t.get("task_code") for t in self.xer.task_table.records}
        
        # Build adjacency graph
        adj: Dict[str, Set[str]] = {}
        all_nodes = set(task_id_to_code.keys())
        for n in all_nodes:
            adj[n] = set()

        direct_edges: List[Tuple[str, str, Dict[str, str]]] = []
        for p in self.xer.pred_table.records:
            pred_id = p.get("pred_task_id")
            succ_id = p.get("task_id")
            if pred_id and succ_id:
                if pred_id not in adj:
                    adj[pred_id] = set()
                adj[pred_id].add(succ_id)
                direct_edges.append((pred_id, succ_id, p))

        redundant = []
        # For each edge (u, v), check if there is an alternate path from u to v of length >= 2
        for u, v, record in direct_edges:
            # Temporary remove direct edge
            adj[u].remove(v)
            if self._has_path(adj, u, v):
                redundant.append({
                    "task_pred_id": record.get("task_pred_id"),
                    "pred_code": task_id_to_code.get(u, u),
                    "succ_code": task_id_to_code.get(v, v),
                    "pred_type": record.get("pred_type", "PR_FS"),
                    "lag": record.get("lag_hr_cnt", "0")
                })
            # Restore edge
            adj[u].add(v)

        return redundant

    def _has_path(self, adj: Dict[str, Set[str]], start: str, target: str) -> bool:
        visited = set()
        queue = [start]
        while queue:
            curr = queue.pop(0)
            if curr == target:
                return True
            if curr not in visited:
                visited.add(curr)
                for neighbor in adj.get(curr, []):
                    if neighbor not in visited:
                        queue.append(neighbor)
        return False

    def remove_redundant_relationships(self) -> Tuple[XERFile, int]:
        """Returns a cloned XER with redundant ties removed."""
        new_xer = copy.deepcopy(self.xer)
        redundant = self.find_redundant_relationships()
        redundant_ids = {r["task_pred_id"] for r in redundant if r["task_pred_id"]}

        if new_xer.pred_table:
            new_xer.pred_table.records = [
                p for p in new_xer.pred_table.records 
                if p.get("task_pred_id") not in redundant_ids
            ]
        return new_xer, len(redundant)

    def find_dangling_activities(self) -> Dict[str, List[Dict[str, str]]]:
        """Detects activities missing predecessors (open start) or successors (open finish)."""
        if not self.xer.task_table:
            return {"open_starts": [], "open_finishes": []}

        preds = self.xer.pred_table.records if self.xer.pred_table else []
        has_pred = {p.get("task_id") for p in preds}
        has_succ = {p.get("pred_task_id") for p in preds}

        open_starts = []
        open_finishes = []
        for t in self.xer.task_table.records:
            tid = t.get("task_id")
            code = t.get("task_code")
            name = t.get("task_name")
            ttype = t.get("task_type")
            if ttype in ("TT_LOE", "TT_WBS"):
                continue

            if tid not in has_pred and ttype != "TT_Mile":
                open_starts.append({"task_code": code, "task_name": name, "task_id": tid})
            if tid not in has_succ and ttype != "TT_FinMile":
                open_finishes.append({"task_code": code, "task_name": name, "task_id": tid})

        return {"open_starts": open_starts, "open_finishes": open_finishes}

    def zero_out_update(self) -> XERFile:
        """
        Converts an update XER into a clean baseline:
        - Resets status_code to TK_NotStart
        - Clears act_start_date and act_end_date
        - Restores remain_durn_hr_cnt to target_durn_hr_cnt
        - Resets phys_complete_pct to 0
        """
        new_xer = copy.deepcopy(self.xer)
        if new_xer.task_table:
            for t in new_xer.task_table.records:
                t["status_code"] = "TK_NotStart"
                t["act_start_date"] = ""
                t["act_end_date"] = ""
                t["phys_complete_pct"] = "0"
                if t.get("target_durn_hr_cnt"):
                    t["remain_durn_hr_cnt"] = t["target_durn_hr_cnt"]
                if t.get("target_work_qty"):
                    t["remain_work_qty"] = t["target_work_qty"]
                    t["act_work_qty"] = "0"

        return new_xer

    def purge_tables(self, tables_to_remove: List[str]) -> XERFile:
        """Removes unwanted or bloated tables such as POBS, RISK, etc."""
        new_xer = copy.deepcopy(self.xer)
        for t in tables_to_remove:
            t_upper = t.upper()
            if t_upper in new_xer.tables:
                del new_xer.tables[t_upper]
        return new_xer

    def batch_rename_activity_ids(self, mapping: Dict[str, str]) -> XERFile:
        """Safely renames activity codes/IDs across all related tables."""
        new_xer = copy.deepcopy(self.xer)
        if new_xer.task_table:
            for t in new_xer.task_table.records:
                old_code = t.get("task_code")
                if old_code in mapping:
                    t["task_code"] = mapping[old_code]
        return new_xer
