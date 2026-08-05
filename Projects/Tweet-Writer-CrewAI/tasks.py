from crewai import Task
from agents import tech_researcher, tweet_writer

research_task = Task(
    description=(
        "Search for the most interesting and recent facts about {topic}. "
        "Summarize the key insights in 3-5 concise bullet points."
    ),
    expected_output="3-5 bullet points with the most interesting facts about {topic}.",
    agent=tech_researcher,
)

tweet_task = Task(
    description=(
        "Using the research, write one tweet about {topic}. "
        "Rules: casual tone, no emojis, max 280 characters, punchy and engaging. "
        "Output ONLY the tweet text — no labels, no quotes, no explanation."
    ),
    expected_output="A single tweet under 280 characters, no emojis, casual and engaging.",
    agent=tweet_writer,
)