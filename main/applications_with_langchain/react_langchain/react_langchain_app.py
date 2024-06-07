from typing import Union

from langchain.agents.format_scratchpad import format_log_to_str
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.tools import render_text_description, Tool

from main.applications_with_langchain.application_interface import Application
from main.utils.utils import override
from langchain.agents import tool
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.agents.output_parsers import ReActSingleInputOutputParser
from main.applications_with_langchain.react_langchain.callbacks import AgentCallbackHandler


@tool
def get_text_length(text: str) -> int:
    """Returns the length of a text by characters"""
    print(f"get_text_length enter with {text=}")
    text = text.strip("'\n").strip(
        '"'
    )  # stripping away non-alphabetic characters just in case
    return len(text)


def find_tool_by_name(tools: list[Tool], tool_name: str) -> Tool:
    for tool in tools:
        if tool.name == tool_name:
            return tool
    raise ValueError(f"Tool with name {tool_name} not found")


class ReactLangchainAppAgent(Application):
    @override
    def run(self, **kwargs):
        print("Hello React langchain!")
        tools = [get_text_length]

        template = """
        Answer the following questions as best you can. You have access to the following tools:

        {tools}
        
        Use the following format:
        
        Question: the input question you must answer
        Thought: you should always think about what to do
        Action: the action to take, should be one of [{tool_names}]
        Action Input: the input to the action
        Observation: the result of the action
        ... (this Thought/Action/Action Input/Observation can repeat N times)
        Thought: I now know the final answer
        Final Answer: the final answer to the original input question
        
        Begin!
        
        Question: {input}
        Thought: {agent_scratchpad}
        """

        prompt = PromptTemplate.from_template(template=template).partial(
            tools=render_text_description(tools), tool_names=",".join([t.name for t in tools])
        )

        llm = ChatOpenAI(
            temperature=0,
            model_kwargs={"stop": ["\nObservation", "Observation"]},
            callbacks=[AgentCallbackHandler()]
        )
        intermediate_steps = []

        agent = (
                {
                    "input": lambda x: x["input"],
                    "agent_scratchpad": lambda x: format_log_to_str(x["agent_scratchpad"])
                }
                | prompt
                | llm
                | ReActSingleInputOutputParser()
        )

        agent_step = ""

        while not isinstance(agent_step, AgentFinish):

            agent_step: Union[AgentAction, AgentFinish] = agent.invoke(
                {
                    "input": "What is the length of 'DOG' in characters?",
                    "agent_scratchpad": intermediate_steps,
                }
            )

            print(agent_step)

            if isinstance(agent_step, AgentAction):
                tool_name = agent_step.tool
                tool_to_use = find_tool_by_name(tools, tool_name)
                tool_input = agent_step.tool_input
                observation = tool_to_use.func(str(tool_input))
                print(f"{observation=}")
                intermediate_steps.append((agent_step, str(observation)))

        print(agent_step)
