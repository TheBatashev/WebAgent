# Third-party imports
from dotenv import load_dotenv, find_dotenv
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.messages.utils import trim_messages, count_tokens_approximately
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.prebuilt.chat_agent_executor import AgentState
from langgraph.checkpoint.memory import InMemorySaver
from langchain_tavily import TavilySearch
from langgraph.graph import StateGraph


from config import OpenAIConfig
from prompts import WEB_AGENT_SYSTEM_PROMPT


MODEL_NAME: str = OpenAIConfig.model_name
CHAT_HISTORY_TOKENS: int = OpenAIConfig.chat_history_tokens
RECURSION_LIMIT: int = OpenAIConfig.recursion_limit


model = ChatOpenAI(
    model=OpenAIConfig.model_name, 
    api_key=OpenAIConfig.api_key)

checkpointer = InMemorySaver()


# This function will be called every time before the node that calls LLM
def trim_history_hook(state: AgentState):
    trimmed_messages = trim_messages(
        state["messages"],
        strategy="last",
        token_counter=count_tokens_approximately,
        max_tokens=CHAT_HISTORY_TOKENS,
        start_on="human",
        end_on=("human", "tool")
    )
    return {"llm_input_messages": trimmed_messages}


def post_model_hook(state: AgentState) -> AgentState:
    return state


def format_user_prompt(user: str) -> str:
    return WEB_AGENT_SYSTEM_PROMPT.format(user=user)


def generate_system_prompt(state: AgentState, config: RunnableConfig):
    try:
        user = config["configurable"].get("user")
    except Exception:
        user = None

    if user is not None:
        system_message_content = format_user_prompt(user)
        new_system_message = SystemMessage(content=system_message_content)
        return [new_system_message] + state["messages"]

    return state["messages"]


async def get_agent():

    
    agent = create_react_agent(
        model=model,
        tools=[TavilySearch(max_results=3)],
        pre_model_hook=trim_history_hook,
        prompt=generate_system_prompt,
    )

    graph = StateGraph(AgentState)

    AGENT = "AGENT"
    POST_MODEL_HOOK = "POST_MODEL_HOOK"

    graph.add_node(AGENT, agent)
    graph.add_node(POST_MODEL_HOOK, post_model_hook)

    graph.set_entry_point(AGENT)
    graph.add_edge(AGENT, POST_MODEL_HOOK)
    graph.set_finish_point(POST_MODEL_HOOK)

    app = graph.compile(checkpointer=checkpointer)

    return app.with_config(recursion_limit=RECURSION_LIMIT)
