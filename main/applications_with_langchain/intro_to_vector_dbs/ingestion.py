from main.applications_with_langchain.application_interface import Application
from main.utils.utils import override


class VectorDbs(Application):
    @override
    def run(self, **kwargs):
        print("Hello Ingesting!")
