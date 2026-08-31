from typing import TextIO
from planbee.parser.xer_parser import XERFile

class XERWriter:
    @staticmethod
    def write_file(xer: XERFile, file_path: str, encoding: str = "latin1") -> None:
        with open(file_path, "w", encoding=encoding, errors="replace", newline="\r\n") as f:
            XERWriter.write_stream(xer, f)

    @staticmethod
    def write_string(xer: XERFile) -> str:
        import io
        stream = io.StringIO()
        XERWriter.write_stream(xer, stream)
        return stream.getvalue()

    @staticmethod
    def write_stream(xer: XERFile, stream: TextIO) -> None:
        if xer.header:
            stream.write(f"{xer.header}\n")
        else:
            stream.write("ERMHDR\t20.12\t1\tEXPORT\tPROJECT\tPlanBee\tAdmin\tStandard\n")
            
        for table_name, table in xer.tables.items():
            if not table.fields or not table.records:
                continue
            stream.write(f"%T\t{table.name}\n")
            stream.write(f"%F\t" + "\t".join(table.fields) + "\n")
            for rec in table.records:
                row_vals = [str(rec.get(f, "")) for f in table.fields]
                stream.write(f"%R\t" + "\t".join(row_vals) + "\n")
                
        stream.write("%E\n")
