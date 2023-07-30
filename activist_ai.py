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


import os, json
import pandas as pd
from urllib.request import urlopen
from collections import defaultdict
from langchain.agents import Tool
from langchain.tools.json.tool import JsonSpec, JsonGetValueTool
from langchain.agents import create_json_agent, create_pandas_dataframe_agent
from langchain.chat_models import ChatAnthropic
from langchain.tools.python.tool import PythonREPLTool, PythonAstREPLTool
from langchain.agents.agent_types import AgentType

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

llm = ChatAnthropic(model='claude-2',
                 temperature=0)

traffic_crashes_url = "https://data.sfgov.org/resource/ubvf-ztfx.csv"

search = DuckDuckGoSearchRun()

tools_internet = [
    Tool(
        name = "Current Search",
        func=search.run,
        description="A tool to answer questions about current events or the current state of the world"
    ),
]

python_tools = [
    Tool(
        name = "REPL",
        func=PythonREPLTool(),
        description="A tool for running python code in a REPL."
    ),
    Tool(
        name = "AST REPL",
        func=PythonAstREPLTool(),
        description="A tool for running python code in a REPL."
    ),
]

df = pd.read_csv(traffic_crashes_url)
traffic_light_agent = create_pandas_dataframe_agent(llm, df, tool=python_tools, verbose=True, agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION, memory=memory)
internet_chain = initialize_agent(tools_internet,
                               llm,
                               agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
                               verbose=True,
                               memory=memory)
def should_use_data(prompt):
  messages = [
      HumanMessage(
          content=f"""
          <prompt>
          {prompt}
          </prompt>

          <Question> Is the above prompt about traffic collisions? If so,
          just say "True". Otherwise, say "False". If you are unsure, say "False"
          </Question>
          """
      )
  ]

  return llm(messages).content.strip() == "True"


def query_fn():
    def bot(prompt):
        if should_use_data(prompt):
            return traffic_light_agent.run(input=prompt)
        else:
            return internet_chain.run(input=prompt)
        return internet_chain.run(input=prompt)
    
    return bot
