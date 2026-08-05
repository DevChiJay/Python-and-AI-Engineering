from crewai import Agent, LLM
from tools import duckduckgo_search

# thinking=False prevents <think> blocks that break CrewAI's response parser
llm = LLM(
    model="ollama/qwen3.5",
    base_url="http://localhost:11434",
    extra_body={"think": False},
)

tech_researcher = Agent(
    role="Tech Researcher",
    goal="Find the most interesting and recent facts about a tech topic",
    verbose=True,
    memory=False,
    backstory=(
        "You are a sharp tech journalist who digs up relevant, recent, "
        "and genuinely interesting facts about any tech topic."
    ),
    tools=[duckduckgo_search],
    llm=llm,
    allow_delegation=False
)

tweet_writer = Agent(
    role="Tweet Writer",
    goal="Write one casual, short, engaging tweet — no emojis, max 280 characters",
    verbose=True,
    memory=False,
    backstory=(
        "You are a tech influencer known for punchy, no-fluff tweets "
        "that make people stop scrolling."
    ),
    tools=[],
    llm=llm,
    allow_delegation=False
)