""" 
© 2026 Rozendox. 
All rights reserved.
Proprietary and confidential.  

api_integration_broker.domain.value_objects.payload.py

SINGLE RESPONSIBILITY PRINCIPLE: This module defines the Payload value object,

which encapsulates the data structure for the payload being processed in the integration flow.
"""

from dataclasses import dataclass
from typing import Dict, Any

@dataclass(frozen=True)
class Payload:
    """Objeto de Valor imutavel contendo os dados trafegados."""
    content: Dict[str, Any]
    schema_version: str

    def is_empty(self) -> bool:
        return not bool(self.content)
