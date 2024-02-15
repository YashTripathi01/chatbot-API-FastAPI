from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI

from core.config import settings

# instantiating the openai llm model
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo-1106",
    temperature=0,
    max_tokens=150,
    api_key=settings.OPENAI_API_KEY,
)

# adding buffer memory
conversation_buffer_window = ConversationChain(
    llm=llm,
    memory=ConversationBufferWindowMemory(
        k=3
    ),  # k=3, store last 3 conversations in the memory
    verbose=True,
)
