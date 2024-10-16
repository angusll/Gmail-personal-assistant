from .prompt import prompt_template
from .llm import llm_client
from langchain.output_parsers import OutputFixingParser
from langchain_core.output_parsers import JsonOutputParser
from .data_model import PythonCode

parser = JsonOutputParser(pydantic_object=PythonCode)
output_fixer = OutputFixingParser.from_llm(parser=parser, llm=llm_client)

chain = prompt_template | llm_client | output_fixer
