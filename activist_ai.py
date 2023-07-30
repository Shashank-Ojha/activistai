from langchain.chat_models import ChatAnthropic
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import AIMessage, HumanMessage, SystemMessage

from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatAnthropic
from langchain.agents import Tool
from langchain.agents import AgentType
from langchain.tools import DuckDuckGoSearchRun
from langchain.agents import initialize_agent

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

llm = ChatAnthropic(model='claude-2',
                 temperature=0)


search = DuckDuckGoSearchRun()
tools = [
    Tool(
        name = "Current Search",
        func=search.run,
        description="useful for when you need to answer questions about current events or the current state of the world"
    ),
]

agent_chain = initialize_agent(tools,
                               llm,
                               agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
                               verbose=True,
                               memory=memory)

def query_fn():
    def research_bot(prompt):
        return agent_chain.run(input=prompt)
    return research_bot
