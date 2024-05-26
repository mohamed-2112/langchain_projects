from main.applications_with_langchain.application_interface import Application
from main.constants.informations import Informations



class ApplicationRunner:
    def __init__(self , application: Application):
        self.application = application
    
    def langchainTestApp(self):
        information = Informations.information_1
        self.application.run(information = information)

    def ice_breaker_app(self):
        profile_url = 'https://linkedin.com/in/johnrmarty/'
        self.application.run(profile_url=profile_url)