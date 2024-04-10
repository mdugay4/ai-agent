import logging
import sys
from dotenv import load_dotenv
from llama_index.core import SummaryIndex
from llama_index.readers.web import SimpleWebPageReader
# import os

load_dotenv()

# logging.basicConfig(stream=sys.stdout, level=logging.INFO)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

documents = SimpleWebPageReader(html_to_text=True).load_data(
    ["https://teamfighttactics.leagueoflegends.com/en-us/news/game-updates/teamfight-tactics-patch-14-7-notes/"],
)

# documents[0]

index = SummaryIndex.from_documents(documents)
# set Logging to DEBUG for more detailed outputs
query_engine = index.as_query_engine()
response = query_engine.query("What augments did they change?")
print(response)