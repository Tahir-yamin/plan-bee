"""
OpenPlanCo Web Dashboard - FastAPI Backend Server
"""

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
import io
import json

from openplanco.parser.xer_parser import XERParser
from openplanco.parser.xer_writer import XERWriter
from openplanco.analyzer.dcma_audit import DCMAAuditor
from openplanco.comparison.schedule_diff import ScheduleComparator
from openplanco.network.cpm_optimizer import CPMOptimizer
from openplanco.converter.excel_xer import ExcelXERConverter

app = FastAPI(
    title="OpenPlanCo API",
    description="REST API for Primavera P6 XER parsing, DCMA 14-Point Audits, S-Curves, and Schedule Comparison",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "OpenPlanCo Backend API is running."}

@app.post("/api/parse-xer")
async def parse_xer(file: UploadFile = File(...)):
    content = await file.read()
    try:
        text = content.decode("latin1")
        xer = XERParser.parse_text(text)
        
        tasks = xer.task_table.records if xer.task_table else []
        preds = xer.pred_table.records if xer.pred_table else []
        wbs = xer.wbs_table.records if xer.wbs_table else []
        
        return {
            "filename": file.filename,
            "project_name": (xer.project_table.records[0].get("proj_short_name", "") if xer.project_table and xer.project_table.records else "Project"),
            "task_count": len(tasks),
            "relationship_count": len(preds),
            "wbs_count": len(wbs),
            "tasks": tasks[:200],
            "relationships": preds[:200],
            "wbs": wbs
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/dcma-audit")
async def dcma_audit(file: UploadFile = File(...)):
    content = await file.read()
    try:
        text = content.decode("latin1")
        xer = XERParser.parse_text(text)
        auditor = DCMAAuditor(xer)
        report = auditor.audit()
        return report
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/compare-xers")
async def compare_xers(baseline: UploadFile = File(...), update: UploadFile = File(...)):
    b_content = await baseline.read()
    u_content = await update.read()
    try:
        b_xer = XERParser.parse_text(b_content.decode("latin1"))
        u_xer = XERParser.parse_text(u_content.decode("latin1"))
        comp = ScheduleComparator(b_xer, u_xer)
        diff = comp.compare()
        return diff
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/clean-xer")
async def clean_xer(file: UploadFile = File(...)):
    content = await file.read()
    try:
        xer = XERParser.parse_text(content.decode("latin1"))
        optimizer = CPMOptimizer(xer)
        cleaned_xer, count = optimizer.remove_redundant_relationships()
        out_str = XERWriter.write_string(cleaned_xer)
        
        return StreamingResponse(
            io.BytesIO(out_str.encode("latin1")),
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename=cleaned_{file.filename}"}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
