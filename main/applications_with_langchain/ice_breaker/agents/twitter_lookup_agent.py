from langchain.prompts.prompt import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from main.applications_with_langchain.ice_breaker.tools.tools import get_profile_url_tavily


class TwitterAgent:
    def __init__(self):
        pass

    def lookup(self, name: str) -> str:
        llm = HuggingFaceEndpoint(repo_id="mistralai/Mistral-7B-Instruct-v0.3", temperature=1)
        template = """given the name {name_of_person} I want you to find a link to their Twitter profile page, and extract from it their username.
        In you Final answer provide only the person's username and nothing else. """

        prompt_template = PromptTemplate(template=template, input_variables=["name_of_person"])

        tools_for_agent = [
            Tool(
                name="Crawl Google 4 Twitter profile page",
                func=get_profile_url_tavily,
                description="useful for when you need to get the Twitter Page URL"
            )
        ]

        react_prompt = hub.pull("hwchase17/react")
        agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, handle_parsing_errors=True, verbose=True)
        result = agent_executor.invoke(
            input={"input": prompt_template.format_prompt(name_of_person=name)},
        )

        linkedin_profile_url = result["output"]
        return linkedin_profile_url
