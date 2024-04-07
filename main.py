from dotenv import load_dotenv
import os
import pandas as pd
from llama_index.core.query_engine import PandasQueryEngine
from prompts import new_prompt, instruction_str, context
from note_engine import note_engine
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI
from pdf import united_states_engine

load_dotenv()

population_path = os.path.join("data", "world_pop_2023.csv")
population_df = pd.read_csv(population_path)

# print(population_df.head())
population_query_engine = PandasQueryEngine(
    df=population_df, verbose=True, instruction_str=instruction_str
)

population_query_engine.update_prompts({"pandas_prompt": new_prompt})
# population_query_engine.query("what is the population of the united states")

tools = [
    note_engine,
    QueryEngineTool(
        query_engine=population_query_engine, 
        metadata=ToolMetadata(
            name="population_data",
            description="this gives information at the world population and demographics"
        ),
    ),
    QueryEngineTool(
        query_engine=united_states_engine, 
        metadata=ToolMetadata(
            name="united_states_data",
            description="this gives information about united states the country"
        ),
    ),
]

llm = OpenAI(model="gpt-3.5-turbo-0613")
agent = ReActAgent.from_tools(tools, llm=llm, verbose=True, context=context)

while True:
    prompt = input("Enter a prompt (q to quit): ")
    if prompt == "q": 
        break
    result = agent.query(prompt)
    print(result)

# todo: add more functions to agent
