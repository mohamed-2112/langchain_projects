from main.applications_with_langchain.application_interface import Application
from main.constants.constant import INFORMATION, PROFILE_URL, LINKEDIN_NAME
from main.applications_with_langchain.documentation_helper_app.ingestion import run_ingestion


class ApplicationRunner:
    def __init__(self, application: Application = None):
        self.application = application

    def langchain_test_app(self):
        information = INFORMATION
        self.application.run(information=information)

    def ice_breaker_app(self):
        self.application.run()

    def react_langchain_app_runner(self):
        self.application.run()

    def rag_runner(self):
        self.application.run()

    def local_vectorstore_pdf_runner(self):
        self.application.run()

    def documentation_helper_ingestion_runner(self):
        run_ingestion()

    def documentation_helper_runner(self):
        query = "What is Retrieval QA chain?"
        self.application.run(query=query)
