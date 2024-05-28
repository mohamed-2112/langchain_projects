import os
from dotenv import load_dotenv
from pathlib import Path
from main.applications_with_langchain.first_langchain_test.testing_langchain import App1
from .applications_runner import ApplicationRunner
from main.applications_with_langchain.ice_breaker.app import IceBreakerApp
from main.applications_with_langchain.react_langchain.react_langchain_app import ReactLangchainAppAgent


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

    # application = App1()
    # application2 = IceBreakerApp()
    application3 = ReactLangchainAppAgent()
    application_runner = ApplicationRunner(application3)
    # applicationRunner.langchain_test_app()
    # application_runner.ice_breaker_app()
    application_runner.react_langchain_app_runner()


if __name__ == '__main__':
    main()
