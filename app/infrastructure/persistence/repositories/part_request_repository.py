from typing import Optional, List
from datetime import datetime

from ..db import get_session
from ..models import PartRequestRecord


class PartRequestRepository:
    def create(self, payload: str, source: Optional[str] = None) -> PartRequestRecord:
        with get_session() as s:
            rec = PartRequestRecord(payload=payload, source=source)
            s.add(rec)
            s.commit()
            s.refresh(rec)
            return rec

    def get(self, req_id: str) -> Optional[PartRequestRecord]:
        with get_session() as s:
            return s.get(PartRequestRecord, req_id)

    def list_recent(self, limit: int = 50) -> List[PartRequestRecord]:
        with get_session() as s:
            stmt = (
                PartRequestRecord.select()
                .order_by(PartRequestRecord.created_at.desc())
                .limit(limit)
            )
            return list(s.exec(stmt))

    def update_status(self, req_id: str, new_status: str) -> Optional[PartRequestRecord]:
        with get_session() as s:
            rec = s.get(PartRequestRecord, req_id)
            if not rec:
                return None
            rec.status = new_status
            rec.updated_at = datetime.utcnow()
            s.add(rec)
            s.commit()
            s.refresh(rec)
            return rec
