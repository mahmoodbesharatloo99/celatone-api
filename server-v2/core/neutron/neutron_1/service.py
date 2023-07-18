from core.base.base_service import BaseService

class Neutron1Service(BaseService):
    chain: str = "neutron"
    network: str = "neutron-1"