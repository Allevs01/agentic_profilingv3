import os
from dotenv import load_dotenv
import time
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, task, crew, before_kickoff
from company_sim.tools.discord_tools import (
    read_discord_messages,
    send_discord_webhook
)
load_dotenv()

from company_sim.utils import discord_logger

# model = os.getenv("MODEL")
gemini_llm = LLM(     model=os.getenv("MODEL_NAME"), base_url=os.getenv("BASE_URL"), api_key=os.getenv("CUSTOM_API_KEY") )


def _step_callback(output) -> None:
    """Callback dopo ogni step dell'agente - aspetta 10 secondi per diminuire rate limiting"""
    time.sleep(5)

@CrewBase
class MarketingCrew:

    @agent
    def marketing_lead(self) -> Agent:
        return Agent(
            config=self.agents_config["marketing_lead"],
            tools=[read_discord_messages,
                   send_discord_webhook],
            verbose=True,
            step_callback=_step_callback,
            llm=gemini_llm
        )

    @agent
    def content_creator(self) -> Agent:
        return Agent(
            config=self.agents_config["content_creator"],
            tools=[read_discord_messages,
                   send_discord_webhook],
            verbose=True,
            step_callback=_step_callback,
            llm=gemini_llm
        )

    @task
    def marketing_lead_reply(self) -> Task:
        return Task(
            config=self.tasks_config["marketing_lead_reply"],
           # callback = discord_logger.task_callback
        )
    
    @task
    def content_creator_reply(self) -> Task:
        return Task(
            config=self.tasks_config["content_creator_reply"],
          #  callback = discord_logger.task_callback
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.marketing_lead(),
                self.content_creator()
            ],
            tasks=[
                self.marketing_lead_reply(),
                self.content_creator_reply()
            ],
            process=Process.sequential,
            planning = True,
            planning_llm = gemini_llm,
            verbose=True
        )
