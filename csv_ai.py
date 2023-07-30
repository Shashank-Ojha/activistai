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

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = "ls__a8143819fcbc46228ef4cf752cd29740"
os.environ["ANTHROPIC_API_KEY"] = "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"
    
# Create a llm model using Claude-2
llm = ChatAnthropic(model='claude-2', temperature=0)

# Traffic Crashes Resulting in Injury 
traffic_crashes_url = "https://data.sfgov.org/resource/ubvf-ztfx.csv"

tools = [
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
agent = create_pandas_dataframe_agent(ChatAnthropic(model='claude-2', temperature=1), df, tool=tools, verbose=True, agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,)
agent.run("Which year and month did we have the most accident.")

