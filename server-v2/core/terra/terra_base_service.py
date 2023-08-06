from core.base.base_service import BaseService
from utils import helper

class TerraBaseService(BaseService):
    def get_balances(self, account_address):
        balance = super().get_balances(account_address)
        + helper.get_hive_balance(self.chain, self.network, account_address)

        return balance
