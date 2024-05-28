import os
from dotenv import load_dotenv
from pathlib import Path
from main.applications_with_langchain.first_langchain_test.testing_langchain import App1
from .applications_runner import ApplicationRunner
from main.applications_with_langchain.ice_breaker.app import IceBreakerApp


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
    application2 = IceBreakerApp()
    application_runner = ApplicationRunner(application2)
    # applicationRunner.langchainTestApp()
    application_runner.ice_breaker_app()


if __name__ == '__main__':
    main()
