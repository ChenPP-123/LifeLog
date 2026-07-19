import uuid
from datetime import datetime


class Log:
    def __init__(self, content, created_at=None, id=None):
        self.content = content
        self.id = id if id is not None else str(uuid.uuid4())
        self.created_at = (
            created_at if created_at is not None else datetime.now().isoformat()
        )
