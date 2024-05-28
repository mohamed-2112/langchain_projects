from main.applications_with_langchain.application_interface import Application
from main.constants.constant import INFORMATION, PROFILE_URL, LINKEDIN_NAME


class ApplicationRunner:
    def __init__(self, application: Application):
        self.application = application

    def langchainTestApp(self):
        information = INFORMATION
        self.application.run(information=information)

    def ice_breaker_app(self):
        self.application.run()
