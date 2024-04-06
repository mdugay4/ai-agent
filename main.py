from dotenv import load_dotenv
import os
import pandas as pd
# from llama_index.query_engine import PandasQueryEngine
from llama_index.core.query_engine import PandasQueryEngine
from prompts import new_prompt, instruction_str, context
from note_engine import note_engine
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI

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
]

llm = OpenAI(model="gpt-3.5-turbo-0613")
agent = ReActAgent.from_tools(tools, llm=llm, verbose=True, context=context)

# walrus operator :=
# while (prompt := input("Enter a prompt (q to quit): ")) != "q":
#     result = agent.query(prompt)
#     print(result)

while True:
    prompt = input("Enter a prompt (q to quit): ")
    if prompt == "q": 
        break
    else: 
        result = agent.query(prompt)
        print(result)

# todo: figure out why it loops over prompt and responds multiple times
# Thought: The current language of the user is: English. I need to use a tool to help me save the note.
# Action: note_saver
# Action Input: {'note': 'I am smart'}
# Observation: note saved
# Observation: Error: Could not parse output. Please follow the thought-action-input format. Try again.
