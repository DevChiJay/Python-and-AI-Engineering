from crewai import Crew, Process
from Learning.CrewAI.agents import senior_researcher, script_writer
from Learning.CrewAI.tasks import research_task, script_task

# Create Crew
crew = Crew(
    agents=[senior_researcher, script_writer], # you are giving two agents
    tasks=[research_task, script_task],
    process=Process.sequential,
    verbose=True
)

# Run Crew
if __name__ == "__main__":

    result = crew.kickoff(
        inputs={
            "topic": "CrewAI Tutorial for Beginners" #this starts the entire workflow
        }
    )

    print("\n\n======== FINAL OUTPUT ========\n")
    print(result)