from dotenv import load_dotenv
from pathlib import Path
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from constants.informations import Informations
from langchain_huggingface import HuggingFaceEndpoint
from applications_with_langchain.first_langchain_test.testing_langchain import App1
from applications_runner import ApplicationRunner

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
    
    application = App1()
    applicationRunner = ApplicationRunner(application)
    applicationRunner.langchainTestApp()
    

if __name__ == '__main__':
    main()