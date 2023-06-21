import ast
import os

LCD_DICT = ast.literal_eval(os.getenv("LCD_DICT", ""))
HIVE_DICT = ast.literal_eval(os.getenv("HIVE_DICT", ""))
GRAPHQL_DICT = ast.literal_eval(os.getenv("GRAPHQL_DICT", ""))
GRAPHQL_TEST_DICT = ast.literal_eval(os.getenv("GRAPHQL_TEST_DICT", ""))
SCANWORKS_URL = os.getenv("SCANWORKS_URL", None)
PRICE_CACHER_URL = os.getenv("PRICE_CACHER_URL", None)
COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY", None)
