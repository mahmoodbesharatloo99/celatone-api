import ast
import os

LCD_DICT = ast.literal_eval(os.getenv("LCD_DICT", ""))
HIVE_DICT = ast.literal_eval(os.getenv("HIVE_DICT", ""))
GRAPHQL_DICT = ast.literal_eval(os.getenv("GRAPHQL_DICT", ""))
GRAPHQL_TEST_DICT = ast.literal_eval(os.getenv("GRAPHQL_TEST_DICT", ""))
PRICE_CACHER_URL = os.environ["PRICE_CACHER_URL"]
WLD_URL = os.environ["WLD_URL"]
ALDUS_URL = os.environ["ALDUS_URL"]
