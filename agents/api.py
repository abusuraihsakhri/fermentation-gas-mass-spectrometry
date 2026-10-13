"""
FastAPI REST API Server for Fermentation Gas Mass Spectrometry.
"""
import logging
from pathlib import Path
from offgas_analyzer.calculations import calculate_offgas
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from .base import AuditLogger, PHIGuard, SecurityException
from .models import SystemTaskPayload, ConsensusDossier
from .supervisor import SystemSupervisor

logger = logging.getLogger(__name__)

supervisor = SystemSupervisor(model_provider="mock")

app = FastAPI(
    title="Fermentation Gas Mass Spectrometry API",
    description="Legacy threshold-based audit and quantitative dry off-gas analysis",
    version="2.1.0",
)



class OffgasCalculationRequest(BaseModel):
    """Dry molar-flow measurement inputs; all gas compositions are fractions 0..1."""
    inlet_flow_mmol_min: float
    inlet_o2: float
    inlet_co2: float
    outlet_o2: float
    outlet_co2: float


class ChatRequest(BaseModel):
    query: str


@app.get("/", include_in_schema=False)
def console_page():
    return FileResponse(Path(__file__).resolve().parent.parent / "web" / "index.html")


@app.get("/health")
def health():
    return {"status": "HEALTHY", "service": "fermentation-gas-mass-spectrometry", "domain": "Clinical & Biomedical AI", "standard": "CAP / CLSI / ISO Standards", "version": "2.1.0"}


@app.get("/metrics")
def metrics():
    return {
        "dossiers_processed_total": len(supervisor.dossier_registry),
        "audit_blocks_total": len(AuditLogger.get_trail()),
        "system_status": "API_AVAILABLE"
    }


@app.post("/api/audit")
def api_audit(payload: SystemTaskPayload):
    try:
        dossier = supervisor.process_task(payload)
        return dossier.to_dict()
    except SecurityException:
        raise HTTPException(status_code=422, detail="Request blocked by security policy")
    except Exception as e:
        logger.error("Audit endpoint error: %s", type(e).__name__)
        raise HTTPException(status_code=500, detail="Internal processing error")


@app.post("/api/chat")
def api_chat(req: ChatRequest):
    try:
        ans = supervisor.query_supervisory_chat(req.query)
        return {"response": ans}
    except SecurityException as e:
        raise HTTPException(status_code=422, detail="Request blocked by security policy")
    except Exception as e:
        logger.error("Chat endpoint error: %s", type(e).__name__)
        raise HTTPException(status_code=400, detail="Invalid request")


@app.get("/api/audit/logs")
def api_audit_logs():
    return {"audit_trail": AuditLogger.get_trail(), "verified": AuditLogger.verify_integrity()}


@app.post("/api/offgas/calculate")
def api_calculate_offgas(req: OffgasCalculationRequest):
    try:
        return calculate_offgas(**req.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
