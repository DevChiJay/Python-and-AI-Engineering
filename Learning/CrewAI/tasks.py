from crewai import Task
from Learning.CrewAI.agents import senior_researcher, script_writer

# Research Task
research_task = Task(
    description="Explain {topic} in 3 simple bullet points.",
    expected_output="3 clear bullet points explaining the topic.",
    agent=senior_researcher,
)

# Script Writing Task
script_task = Task(
    description=("Using the research, create a SHORT YouTube script "
                 "on {topic} with a hook, 2-3 lines explanation, and outro."),
    expected_output="A short and engaging YouTube script.",
    agent=script_writer,
)