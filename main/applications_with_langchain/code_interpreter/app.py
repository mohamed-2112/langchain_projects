from main.applications_with_langchain.application_interface import Application
from main.utils.utils import override


class CodeInter(Application):
    @override
    def run(self, **kwargs):
        print("start code interpreter...")