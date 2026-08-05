from crewai import Agent

senior_researcher = Agent(
    role="Senior Youtube Researcher",
    goal="Explain topics simply",
    verbose=True,
    memory=False,
    backstory="Expert in simplifying AI topics",
    tools=[],
    llm="ollama/llama3",
    allow_delegation=False
)

script_writer = Agent(
    role="YouTube Script Writer",
    goal="Write short scripts",
    verbose=True,
    memory=False,
    backstory="Expert in writing engaging scripts",
    tools=[],
    llm="ollama/llama3",
    allow_delegation=False
)