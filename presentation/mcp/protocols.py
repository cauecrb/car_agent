from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class MCPRequest:
    method: str
    params: Dict[str, Any]
    id: Optional[str] = None

@dataclass
class MCPResponse:
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    id: Optional[str] = None
