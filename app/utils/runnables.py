"""
Custom Runnables
"""

from langchain_core.runnables import RunnableLambda

from app.utils.query_validator import validate_query
from app.utils.query_mapper import map_query

query_validator = RunnableLambda(validate_query)
query_mapper = RunnableLambda(map_query)