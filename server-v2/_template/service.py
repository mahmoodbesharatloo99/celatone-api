from utils.registry import load_and_check_registry_data
from core.base.base_service import BaseService

class TemplateService(BaseService):
    def __init__(self):
        self._field = []

    @property
    def field(self):
        return self._field