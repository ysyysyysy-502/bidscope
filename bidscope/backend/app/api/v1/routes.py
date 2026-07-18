from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.connectors.registry import get_connectors
from app.core.config import settings
from app.domain.schemas import RunRequest
from app.services.intent_parser import parse_intent
from app.services.run_orchestrator import run_query, get_run

router = APIRouter()

@router.get('/health')
def health():
    return {'status': 'ok', 'service': 'bidscope-api'}

@router.post('/intents/parse')
def parse(payload: RunRequest):
    return parse_intent(payload.query)

@router.get('/sources')
async def sources():
    return [await c.healthcheck() for c in get_connectors()]

@router.post('/runs', status_code=202)
async def create_run(payload: RunRequest):
    return await run_query(payload)

@router.get('/runs/{run_id}')
def read_run(run_id: str):
    run = get_run(run_id)
    if not run:
        raise HTTPException(status_code=404, detail='run not found')
    return run

@router.get('/reports/{run_id}/download')
def download_report(run_id: str):
    run = get_run(run_id)
    if not run or not run.report_filename:
        raise HTTPException(status_code=404, detail='report not found')
    path = settings.storage_dir / run.report_filename
    if not path.exists():
        raise HTTPException(status_code=404, detail='file not found')
    return FileResponse(
        path,
        media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        filename=run.report_filename,
    )
