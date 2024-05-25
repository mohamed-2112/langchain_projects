from applications_with_langchain.application_interface import Application
from constants.informations import Informations



class ApplicationRunner:
    def __init__(self , application: Application):
        self.application = application
    
    def langchainTestApp(self):
        information = Informations.information_1
        self.application.run(information = information)