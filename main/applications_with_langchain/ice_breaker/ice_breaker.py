from typing import Tuple, Any

from langchain.prompts.prompt import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint
from main.applications_with_langchain.application_interface import Application
from main.utils.utils import override
from main.applications_with_langchain.ice_breaker.third_parties.linkedin import LinkedinProfileScrapper
from main.applications_with_langchain.ice_breaker.agents.linkedin_lookup_agent import LinkedInAgent
from main.applications_with_langchain.ice_breaker.agents.twitter_lookup_agent import TwitterAgent
from main.applications_with_langchain.ice_breaker.third_parties.twitter import TwitterProfileScrapper
from main.applications_with_langchain.ice_breaker.output_parsers import summary_parser, Summary
from langchain_openai import ChatOpenAI
from langchain_mistralai import ChatMistralAI


class IceBreaker:

    def ice_break_with(self, name: str) -> tuple[Summary, Any]:
        linkedin_data = self.__linkedin_data_summary(name=name)
        twitter_data = self.__twitter_data_summary(name=name)
        summary_template = """given the information about a person or two from linkedin {information}, and twitter posts 
        {twitter_posts} I want you to create: 
        1. a short summary 
        2. two interesting facts about them
        
        Use both information from twitter and linkedin
        \n {format_instructions}
        """
        summary_prompt_template = PromptTemplate(
            input_variables=["information", "twitter_posts"],
            template=summary_template,
            partial_variables={"format_instructions": summary_parser.get_format_instructions()}
        )
        # Choose to use openai or mistral
        #llm = HuggingFaceEndpoint(repo_id="mistralai/Mistral-7B-Instruct-v0.3", temperature=1)
        llm = ChatOpenAI(temperature=0)
        chain = summary_prompt_template | llm | summary_parser
        res: Summary = chain.invoke(input={"information": linkedin_data, "twitter_posts": twitter_data})
        return res, linkedin_data.get("profile_pic_url")

    def __linkedin_data_summary(self, name: str):
        linkedin_lookup_agent = LinkedInAgent()
        linkedin_username = linkedin_lookup_agent.lookup(name=name)
        linkedin_scrapper = LinkedinProfileScrapper()
        linkedin_username = linkedin_username.replace("</s>", "")
        print(linkedin_username)
        linkedin_data = linkedin_scrapper.scrape_linkedin_profile(linkedin_profile_url=linkedin_username, mock=True)
        return linkedin_data

    def __twitter_data_summary(self, name: str):
        twitter_lookup_agent = TwitterAgent()
        twitter_username = twitter_lookup_agent.lookup(name=name)
        print(twitter_username)
        twitter_username = twitter_username.replace("</s>", "")
        print(twitter_username)
        twitter_scrapper = TwitterProfileScrapper(username=twitter_username)
        twitter_data = twitter_scrapper.scrape_user_tweets(mock=True)
        print("this the twitter data")
        print(twitter_data)
        return twitter_data
