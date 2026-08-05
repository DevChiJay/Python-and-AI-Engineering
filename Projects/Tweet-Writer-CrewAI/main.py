import sys
import os
import tweepy
from dotenv import load_dotenv
from crewai import Crew, Process
from agents import tech_researcher, tweet_writer
from tasks import research_task, tweet_task

load_dotenv()

crew = Crew(
    agents=[tech_researcher, tweet_writer],
    tasks=[research_task, tweet_task],
    process=Process.sequential,
    verbose=True
)


def post_tweet(text: str) -> None:
    client = tweepy.Client(
        consumer_key=os.getenv("TWITTER_API_KEY"),
        consumer_secret=os.getenv("TWITTER_API_SECRET"),
        access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
        access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
    )
    response = client.create_tweet(text=text)
    print(f"\nTweet posted! ID: {response.data['id']}")


if __name__ == "__main__":
    topic = sys.argv[1] if len(sys.argv) > 1 else input("Enter a tech topic: ")

    result = crew.kickoff(inputs={"topic": topic})

    tweet_text = result.raw.strip()
    print("\n\n======== TWEET DRAFT ========\n")
    print(tweet_text)
    print(f"\nCharacter count: {len(tweet_text)}")

    confirm = input("\nPost this tweet? (y/n): ")
    if confirm.lower() == "y":
        post_tweet(tweet_text)
    else:
        print("Tweet not posted.")