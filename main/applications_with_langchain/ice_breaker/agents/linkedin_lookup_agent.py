from langchain.prompts.prompt import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint
from main.utils.utils import override
from main.applications_with_langchain.ice_breaker.third_parties.linkedin import LinkedinProfileScrapper
from langchain_core.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from main.applications_with_langchain.ice_breaker.tools.tools import get_profile_url_tavily


class LinkedInAgent:
    def __init__(self):
        pass

    def lookup(self, name: str) -> str:
        llm = HuggingFaceEndpoint(repo_id="mistralai/Mistral-7B-Instruct-v0.3", temperature=1)
        template = """given the full name {name_of_person} I want you to get me a link to their Linkedin profile 
        page. Your answer should contain only a URL and nothing else just the URL not even in a <url> and don't write 
        </s> after the url"""

        prompt_template = PromptTemplate(template=template, input_variables=["name_of_person"])

        tools_for_agent = [
            Tool(
                name="Crawl Google 4 linkedin profile page",
                func=get_profile_url_tavily,
                description="useful for when you need to get the Linkedin Page URL"
            )
        ]

        react_prompt = hub.pull("hwchase17/react")
        agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)
        result = agent_executor.invoke(input={"input": prompt_template.format_prompt(name_of_person=name)})

        linkedin_profile_url = result["output"]
        return linkedin_profile_url
