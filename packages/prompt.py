from langchain_core.prompts import PromptTemplate
from .output_parser import parser

system_prompt = """ You are an expert python engineer. Your job is to generate code based on user's query {query}.
                    Only respond in the format {{"query": users query, "code": the generated code}}."""

prompt_template = PromptTemplate(
    template=system_prompt,
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)
