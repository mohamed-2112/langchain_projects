from langchain.prompts.prompt import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint
from ..application_interface import Application
from main.utils.utils import override
from main.applications_with_langchain.ice_breaker.third_parties.linkedin import LinkedinProfileScrapper


class IceBreaker(Application):

    @override
    def run(self, **kwargs):
        summary_template = """
        given the LinkedIn information {information} about a person from I want you to create:
        1. a short summary
        2. two interesting facts about them
    """
        summary_prompt_template = PromptTemplate(input_variables=["information"], template=summary_template)
        # Choose to use openai or mistral
        llm = HuggingFaceEndpoint(repo_id="mistralai/Mistral-7B-Instruct-v0.3", temperature=1)
        chain = summary_prompt_template | llm
        profile_url = kwargs["profile_url"]
        linkedin_scrapper = LinkedinProfileScrapper()
        linkedin_data = linkedin_scrapper.scrape_linkedin_profile(linkedin_profile_url=profile_url, mock=True)
        res = chain.invoke(input={"information": linkedin_data})
        print(res)
