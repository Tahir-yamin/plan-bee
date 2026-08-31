from typing import Dict, List, Any, Optional
import os
import io

class XERTable:
    def __init__(self, name: str, fields: Optional[List[str]] = None):
        self.name: str = name
        self.fields: List[str] = fields or []
        self.records: List[Dict[str, str]] = []
        
    def add_record(self, values: List[str]) -> Dict[str, str]:
        record: Dict[str, str] = {}
        for idx, field in enumerate(self.fields):
            record[field] = values[idx] if idx < len(values) else ""
        self.records.append(record)
        return record

    def to_dict_list(self) -> List[Dict[str, str]]:
        return self.records

    def __len__(self) -> int:
        return len(self.records)

    def __repr__(self) -> str:
        return f"<XERTable {self.name} (fields={len(self.fields)}, records={len(self.records)})>"

class XERFile:
    def __init__(self):
        self.header: str = "ERMHDR\t20.12\t1\tEXPORT\tPROJECT\tOpenPlanCo Engine\tAdministrator\tStandard"
        self.tables: Dict[str, XERTable] = {}
        
    def get_table(self, name: str) -> Optional[XERTable]:
        return self.tables.get(name.upper())

    def get_or_create_table(self, name: str, fields: Optional[List[str]] = None) -> XERTable:
        name = name.upper()
        if name not in self.tables:
            self.tables[name] = XERTable(name, fields)
        elif fields:
            self.tables[name].fields = fields
        return self.tables[name]

    @property
    def project_table(self) -> Optional[XERTable]:
        return self.get_table("PROJECT")

    @property
    def task_table(self) -> Optional[XERTable]:
        return self.get_table("TASK")

    @property
    def pred_table(self) -> Optional[XERTable]:
        return self.get_table("TASKPRED")

    @property
    def wbs_table(self) -> Optional[XERTable]:
        return self.get_table("PROJWBS")

    @property
    def rsrc_table(self) -> Optional[XERTable]:
        return self.get_table("TASKRSRC")

    @property
    def calendar_table(self) -> Optional[XERTable]:
        return self.get_table("CALENDAR")

class XERParser:
    @staticmethod
    def parse_file(file_path: str, encoding: str = "latin1") -> XERFile:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"XER file not found: {file_path}")
            
        encodings = [encoding, "utf-8", "cp1252", "latin1"]
        for enc in encodings:
            try:
                with open(file_path, "r", encoding=enc, errors="replace") as f:
                    return XERParser.parse_stream(f)
            except Exception:
                continue
        raise ValueError(f"Failed to parse XER file: {file_path}")

    @staticmethod
    def parse_text(content: str) -> XERFile:
        return XERParser.parse_stream(io.StringIO(content))

    @staticmethod
    def parse_stream(stream: io.TextIOBase) -> XERFile:
        xer = XERFile()
        current_table: Optional[XERTable] = None
        
        for line in stream:
            line_str = line.rstrip("\r\n")
            if not line_str:
                continue
                
            if line_str.startswith("ERMHDR"):
                xer.header = line_str
                continue
                
            if line_str.startswith("%T\t") or line_str.startswith("%T "):
                parts = line_str.split("\t", 1) if "\t" in line_str else line_str.split(" ", 1)
                table_name = parts[1].strip().upper()
                current_table = xer.get_or_create_table(table_name)
                continue
                
            if line_str.startswith("%F\t") or line_str.startswith("%F "):
                if current_table is None:
                    continue
                parts = line_str.split("\t")
                fields = [p.strip() for p in parts[1:]]
                current_table.fields = fields
                continue
                
            if line_str.startswith("%R\t") or line_str.startswith("%R "):
                if current_table is None:
                    continue
                parts = line_str.split("\t")
                values = parts[1:]
                current_table.add_record(values)
                continue
                
            if line_str.startswith("%E"):
                break
                
        return xer
