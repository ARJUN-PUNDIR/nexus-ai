from langchain_core.runnables import (
    RunnableLambda,
    RunnableParallel,
)

from app.services.multi_search import (
    search_gpt,
    search_claude,
    search_general,
)

parallel_search = RunnableParallel(

    general=RunnableLambda(search_general),

    gpt=RunnableLambda(search_gpt),

    claude=RunnableLambda(search_claude),

)