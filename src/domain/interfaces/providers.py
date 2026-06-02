""" 
© 2026 Rozendox. 
All rights reserved.
Proprietary and confidential.  

api_integration_broker.domain.interfaces.providers.py

A estratégia de extensibilidade baseia-se no Princípio Aberto-Fechado (OCP). 
O domínio define o contrato que qualquer provedor externo deve implementar
e a assinatura do Factory Pattern. Novos provedores são adicionados 
à infraestrutura sem modificar as regras de negócio core.

SINGLE RESPONSIBILITY PRINCIPLE: 

"""

from abc import ABC, abstractmethod
from typing import Any, Dict
from src.domain.value_objects.payload import Payload


class IntegrationProvider(ABC):
    """
    Interface for integration providers. 
    Any external provider must implement this interface.
    """
    
    @abstractmethod
    async def send_payload(self, payload: Payload, destination_config: Dict[str, Any]) -> Dict[str, Any]:
        """Envia o payload transformado para o sistema de destino."""
        pass

    @abstractmethod
    async def fetch_payload(self, source_config: Dict[str, Any]) -> Payload:
        """Busca dados brutos do sistema de origem."""
        pass


class ProviderFactory(ABC):
    """Interface para a fabrica abstrata de provedores."""
    
    @abstractmethod
    def get_provider(self, provider_type: str) -> IntegrationProvider:
        """Retorna a instancia correta do provedor baseado no tipo."""
        pass
