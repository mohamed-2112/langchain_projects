import os
from dotenv import load_dotenv
from pathlib import Path

from main.applications_with_langchain.faiss_local_vectorstore.local_vectorstore import LocalVector
from main.applications_with_langchain.first_langchain_test.testing_langchain import App1
from .applications_runner import ApplicationRunner
from main.applications_with_langchain.ice_breaker.app import IceBreakerApp
from main.applications_with_langchain.react_langchain.react_langchain_app import ReactLangchainAppAgent
from main.applications_with_langchain.intro_to_vector_dbs.rag import RAG
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """
    Main function to run the application.
    This is the entry point.
    """
    load_environment()

    switch = {
        1: case1,
        2: case2,
        3: case3,
        4: case4,
        5: case5,
    }
    try:
        application = int(input("""
Hello, choose which application you want to run by choosing a number:
1. first langchain test in the course
2. ice breaker app
3. react langchain agent
4. intro to vector dbs
5. faiss local vectorstore with pdf
- any other choice will close the program.
"""))
        switch.get(application, case_default)()  # Default case is called if the key doesn't exist
    except ValueError:
        logger.error("Invalid input. Please enter a number.")
        case_default()


def load_environment():
    """
    Load environment variables from the .env file.
    """
    env_path = Path('config') / '.env'
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
        logger.info("Environment variables loaded from .env file.")
    else:
        logger.warning(".env file not found. Make sure to create one if environment variables are needed.")


def case1():
    """
    Run the first langchain test application.
    """
    application = App1()
    application_runner = ApplicationRunner(application)
    application_runner.langchain_test_app()


def case2():
    """
    Run the ice breaker application.
    """
    application = IceBreakerApp()
    application_runner = ApplicationRunner(application)
    application_runner.ice_breaker_app()


def case3():
    """
    Run the react langchain agent application.
    """
    application = ReactLangchainAppAgent()
    application_runner = ApplicationRunner(application)
    application_runner.react_langchain_app_runner()


def case4():
    """
    Run the intro to vector dbs application.
    """
    application = RAG()
    application_runner = ApplicationRunner(application)
    application_runner.rag_runner()


def case5():
    """
    Run the local vectorstore with pdf
    """
    application = LocalVector()
    application_runner = ApplicationRunner(application)
    application_runner.local_vectorstore_pdf_runner()


def case_default():
    """
    Handle the default case when an invalid choice is made.
    """
    logger.info("Invalid choice. Exiting the program.")


if __name__ == '__main__':
    main()
