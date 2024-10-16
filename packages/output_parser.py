from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser
from .data_model import PythonCode
from .llm import llm_client

parser = JsonOutputParser(pydantic_object=PythonCode)
output_fixing_parser = OutputFixingParser.from_llm(parser=parser, llm=llm_client)
