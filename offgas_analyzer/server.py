"""
FastAPI REST API Server for OffGas-Analyzer: Fermentation Respiratory Quotient (RQ) & OUR/CER Agent.
"""
from offgas_analyzer.calculations import calculate_offgas
from typing import Dict, Any
from .models import FrontierPayload
from .agents import OffGasCoordinator

coordinator = OffGasCoordinator()


def create_app():
    try:
        from fastapi import FastAPI
        from pydantic import BaseModel

        app = FastAPI(
            title="OffGas-Analyzer: Fermentation Respiratory Quotient (RQ) & OUR/CER Agent",
            description="Calculates Oxygen Uptake Rate (OUR), Carbon Dioxide Evolution Rate (CER), and Respiratory Quotient (RQ = CER/OUR).",
            version="2.1.0",
        )

        class TaskRequest(BaseModel):
            task_id: str = "TASK-2026-001"
            target_identifier: str = "TARGET-BIO-KEY"
            primary_metric: float = 28.5
            secondary_metric: float = 14.2
            status_descriptor: str = "DISCORDANT_ANOMALY"
            is_critical_flag: bool = True
            attributes: Dict[str, Any] = {}


        class OffgasCalculationRequest(BaseModel):
            """Dry molar-flow measurement inputs; all gas compositions are fractions 0..1."""
            inlet_flow_mmol_min: float
            inlet_o2: float
            inlet_co2: float
            outlet_o2: float
            outlet_co2: float

        class ChatRequest(BaseModel):
            query: str

        @app.get("/health")
        def health():
            return {"status": "HEALTHY", "system": "fermentation-gas-mass-spectrometry", "domain": "Bioprocess Engineering", "version": "2.1.0"}

        @app.post("/api/audit")
        def api_audit(req: TaskRequest):
            payload = FrontierPayload(
                task_id=req.task_id,
                target_identifier=req.target_identifier,
                primary_metric=req.primary_metric,
                secondary_metric=req.secondary_metric,
                status_descriptor=req.status_descriptor,
                is_critical_flag=req.is_critical_flag,
                attributes=req.attributes,
            )
            return coordinator.process(payload)

        @app.post("/api/offgas/calculate")
        def api_calculate_offgas(req: OffgasCalculationRequest):
            from fastapi import HTTPException
            try:
                return calculate_offgas(**req.model_dump())
            except ValueError as exc:
                raise HTTPException(status_code=422, detail=str(exc))

        @app.post("/api/chat")
        def api_chat(req: ChatRequest):
            return {"response": coordinator.query_supervisory_chat(req.query)}

        return app
    except ImportError:
        return None
