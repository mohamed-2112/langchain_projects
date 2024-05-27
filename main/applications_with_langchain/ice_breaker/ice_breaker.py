from langchain.prompts.prompt import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint
from ..application_interface import Application
from main.utils.utils import override
from main.applications_with_langchain.ice_breaker.third_parties.linkedin import LinkedinProfileScrapper
from main.applications_with_langchain.ice_breaker.agents.linkedin_lookup_agent import LinkedInAgent


class IceBreaker(Application):

    @override
    def run(self, **kwargs):
        person_name = kwargs["name"]
        response = self.ice_break_with(person_name)

    def ice_break_with(self, name: str) -> str:
        linkedin_lookup_agent = LinkedInAgent()
        linkedin_username = linkedin_lookup_agent.lookup(name=name)
        linkedin_scrapper = LinkedinProfileScrapper()
        print(linkedin_username)
        linkedin_username = linkedin_username.replace("</s>", "")
        print(linkedin_username)
        linkedin_data = linkedin_scrapper.scrape_linkedin_profile(linkedin_profile_url=linkedin_username, mock=True)
        summary_template = """
        given the LinkedIn information {information} about a person from I want you to create:
        1. a short summary
        2. two interesting facts about them
    """
        summary_prompt_template = PromptTemplate(input_variables=["information"], template=summary_template)
        # Choose to use openai or mistral
        llm = HuggingFaceEndpoint(repo_id="mistralai/Mistral-7B-Instruct-v0.3", temperature=1)
        chain = summary_prompt_template | llm
        res = chain.invoke(input={"information": linkedin_data})
        print(res)
        return res
