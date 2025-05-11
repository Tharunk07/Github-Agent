from langchain_community.agent_toolkits.github.toolkit import GitHubToolkit
from langchain_community.utilities.github import GitHubAPIWrapper
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from config import Config


async def perform_github_agent_process(user_message):

    github = GitHubAPIWrapper(github_app_id=Config.GITHUB_APP_ID,
                            github_app_private_key=Config.GITHUB_APP_PRIVATE_KEY,
                            github_repository=Config.GITHUB_REPOSITORY)

    toolkit = GitHubToolkit.from_github_api_wrapper(github, include_release_tools = True)

    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key="your_api_key_here")
    
    tools = [tool for tool in toolkit.get_tools() if tool.name == "Get Issue"]
    assert len(tools) == 1
    tools[0].name = "get_issue"

    agent_executor = create_react_agent(llm, tools)

    example_query = user_message

    events = agent_executor.stream(
        {"messages": [("user", example_query)]},
        stream_mode="values",
    )
    for event in events:
        print(event["messages"][-1].pretty_print())
        event["messages"][-1].pretty_print()



