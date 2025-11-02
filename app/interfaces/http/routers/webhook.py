import os
import json
from typing import Optional

from fastapi import APIRouter, HTTPException, Request, Query, Response
from ...core import llm_client
from ...infrastructure.persistence.repositories.part_request_repository import (
    PartRequestRepository,
)

router = APIRouter(prefix="/webhook", tags=["whatsapp"])
VERIFY_TOKEN = os.getenv("WABA_VERIFY_TOKEN", "dev-token")


@router.get("")
async def verify(
    hub_mode: Optional[str] = Query(None, alias="hub.mode"),
    hub_challenge: Optional[str] = Query(None, alias="hub.challenge"),
    hub_verify_token: Optional[str] = Query(None, alias="hub.verify_token"),
):
    """
    Verificação do webhook do WhatsApp Cloud API.
    """
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        # WhatsApp espera o challenge como texto puro
        return Response(content=str(hub_challenge or ""), media_type="text/plain")
    raise HTTPException(status_code=403, detail="Verification failed")


@router.post("")
async def receive(request: Request):
    """
    Recebe mensagens do WhatsApp, extrai JSON estruturado via OpenAI
    e persiste numa tabela simples (PartRequest).
    """
    body = await request.json()
    try:
        entry = body["entry"][0]["changes"][0]["value"]
        messages = entry.get("messages", [])
        if not messages:
            return {"status": "no_messages"}

        msg = messages[0]
        if msg.get("type") != "text":
            return {"status": "ignored_non_text"}

        user_text = msg["text"]["body"]
        wa_from = msg.get("from")

        # 1) Extrai JSON estruturado (LLM)
        structured = llm_client.extract_part_request(
            user_text, hints={"channel": "whatsapp", "from": wa_from}
        )

        # 2) Persiste
        repo = PartRequestRepository()
        rec = repo.create(payload=json.dumps(structured, ensure_ascii=False), source=wa_from)

        # 3) (Opcional) enviar confirmação ao usuário via WhatsApp Send API
        return {"status": "ok", "request_id": rec.id, "structured": structured}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Webhook parse error: {e}")
