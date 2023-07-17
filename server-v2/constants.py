import ast
import os

LCD_DICT = ast.literal_eval('')
HIVE_DICT = ast.literal_eval()
GRAPHQL_DICT = ast.literal_eval()
GRAPHQL_TEST_DICT = ast.literal_eval()
SCANWORKS_URL = os.getenv("SCANWORKS_URL", None)
PRICE_CACHER_URL = ''
COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY", None)