from dotenv import load_dotenv
from pathlib import Path
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEndpoint
from ..application_interface import Application
from utils.utils import Utils

class App1(Application):
  
  @Utils.override
  def run(self,**kwargs):
    summary_template = """
        given the information {information} about a person from I want you to create:
        1. a short summary
        2. two interesting facts about them
    """
    summary_prompt_template = PromptTemplate(input_variables=["information"], template=summary_template)
    # Choose to use openai or mistral
    #llm = ChatOpenAI(temperature=0)
    llm = HuggingFaceEndpoint(repo_id="mistralai/Mistral-7B-Instruct-v0.3",temperature= 0.9, max_length= 64)
    chain = summary_prompt_template | llm 
    res = chain.invoke(input={"information":kwargs["information"]})
    print(res)