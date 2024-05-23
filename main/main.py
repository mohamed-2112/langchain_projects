from dotenv import load_dotenv
from pathlib import Path
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from constants.informations import Informations
from langchain_huggingface import HuggingFaceEndpoint

def main():
    """
    Main function to run the application.
    This is the entry point.
    """
    # 0. Load environment variables from the file 
    # Define the path to the .env file
    env_path = Path('config') / '.env'

    # Load the .env file
    load_dotenv(dotenv_path=env_path)  
    
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
    res = chain.invoke(input={"information":Informations.information_1})
    print(res)

if __name__ == '__main__':
    main()