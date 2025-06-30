# from langchain.agents import create_react_agent
# from langchain.agents import AgentExecutor
# from langchain.agents.output_parsers import ReActSingleInputOutputParser
# from langchain.prompts import PromptTemplate
# from langchain_core.tools import tool
# from langchain.llms.base import LLM
# from euri_llm import euri_completion
# @tool
# def expert_writer(input):
#     """this is my expert writer """
#     message = [{"role":"user","content" : f"write a sort poen on {input}"}]
#     return euri_completion(messages=message)

# @tool
# def expert_math(input):
#     """this is my expert math tools """
#     result = eval(input,{"__builtins__":{}},{})
#     return result

# tools = [expert_writer, expert_math]
# tools = [expert_writer,expert_math]

# class EuriaiLLM(LLM):
#     def _call(self, prompt, stop=None):
#         return euri_completion([{"role": "user", "content": prompt}])

#     @property
#     def _llm_type(self):
#         return "euri-llm"


# prompt = PromptTemplate.from_template(
#     """You are an intelligent agent with access to tools: {tool_names}

# {tools}

# Use this format strictly:
# Thought: describe what you want to do
# Action: the tool to use, one of [{tool_names}]
# Action Input: the input in JSON format, e.g., {{"input": "2+2"}}
# Observation: result of the action
# ... (repeat Thought/Action/Observation if needed)
# Thought: I now know the final answer
# Final Answer: the final response to the user

# Begin!

# Question: {input}
# {agent_scratchpad}"""
# )

# agent  = create_react_agent(
#     llm = EuriaiLLM(),
#     tools = tools,
#     prompt = prompt,
#     output_parser = ReActSingleInputOutputParser()
# )

# executor = AgentExecutor(
#     agent = agent,
#     tools = tools,
#     verbose = True,
#     handle_parsing_error= True
# )

# response = executor.invoke({"input" : "give me a poem based on earth and try to execure 4*6"})

# print(response['output'])

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

from langchain.agents import create_react_agent, AgentExecutor
from langchain.agents.output_parsers import ReActSingleInputOutputParser
from langchain.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain.llms.base import LLM
from euri_llm import euri_completion  # make sure this works

# Expert Writer Tool
@tool
def expert_writer(input: str) -> str:
    """Generate a short poem about a given topic."""
    messages = [{"role": "user", "content": f"Write a short poem about {input}"}]
    return euri_completion(messages=messages)

# Expert Math Tool
@tool
def expert_math(input: str) -> str:
    """Safely calculate a basic math expression."""
    try:
        result = eval(input, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

tools = [expert_writer, expert_math]

# Custom LLM wrapper
class EuriaiLLM(LLM):
    def _call(self, prompt: str, stop=None) -> str:
        return euri_completion([{"role": "user", "content": prompt}])
    
    @property
    def _llm_type(self) -> str:
        return "euri-llm"

# Prompt with strict ReAct format
prompt = PromptTemplate.from_template(
    """You are an intelligent agent with access to tools: {tool_names}

{tools}

Follow this format strictly:

Thought: describe what you want to do
Action: the tool to use, one of [{tool_names}]
Action Input: the input in JSON format, e.g., {{"input": "earth"}}
Observation: result of the action
... (repeat Thought/Action/Observation as needed)
Thought: I now know the final answer
Final Answer: the final response to the user. NEVER include Action and Final Answer together.

Begin!

Question: {input}
{agent_scratchpad}"""
)

# Create ReAct Agent
agent = create_react_agent(
    llm=EuriaiLLM(),
    tools=tools,
    prompt=prompt,
    output_parser=ReActSingleInputOutputParser()
)

# Agent Executor
executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True
)

# Invoke the agent
response = executor.invoke({
    "input": "Write a poem about Earth and calculate 4*6"
})

# Print final response
print("\n🧠 Final Response:\n")
print(response["output"])

