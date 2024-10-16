import os
import dotenv
from langchain_openai.llms.base import OpenAI

dotenv.load_dotenv()


llm_client = OpenAI(
    base_url=os.environ["LLM_HOST_URL"],
    api_key=os.environ["API_TOKEN"],
    model=os.environ["MODEL_NAME"],
)
