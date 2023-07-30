import os
import pandas as pd
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatAnthropic
from langchain.document_loaders import CSVLoader
from langchain.agents import create_csv_agent

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = "ls__a8143819fcbc46228ef4cf752cd29740"
os.environ["ANTHROPIC_API_KEY"] = "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"

traffic_injuries = pd.read_csv("https://data.sfgov.org/resource/ubvf-ztfx.csv")
traffic_injuries.to_csv("injuries_data.csv")

df = pd.read_csv("https://data.sfgov.org/resource/ubvf-ztfx.csv")
df.to_csv("injuries_data.csv")

agent = create_csv_agent(ChatAnthropic(model="claude-2"), ['injuries_data.csv'], verbose=True)
agent.run("How many rows are there in this csv file?")

