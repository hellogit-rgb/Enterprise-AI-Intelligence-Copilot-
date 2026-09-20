from typing import Any, Dict


def can_access_document(document: Dict[str, Any], role: str) -> bool:
    allowed_roles = document.get('allowed_roles')
    if not allowed_roles:
        return True
    return role in allowed_roles or 'admin' in allowed_roles
