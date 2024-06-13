from main.applications_with_langchain.application_interface import Application
from main.constants.constant import INFORMATION, PROFILE_URL, LINKEDIN_NAME


class ApplicationRunner:
    def __init__(self, application: Application):
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
