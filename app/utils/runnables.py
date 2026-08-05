"""
Custom Runnables
"""

from langchain_core.runnables import RunnableLambda

from app.utils.query_validator import validate_query
from app.utils.query_mapper import map_query
from app.services.research_service import build_context
query_validator = RunnableLambda(validate_query)
query_mapper = RunnableLambda(map_query)
context_builder = RunnableLambda(build_context)