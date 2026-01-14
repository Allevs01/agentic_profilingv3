import os
from dotenv import load_dotenv
import time
from crewai import Agent, Crew, Process, Task, LLM, TaskOutput
from crewai.project import CrewBase, agent, task, crew, before_kickoff
from company_sim.tools.discord_tools import (
    read_discord_messages,
    send_discord_webhook
)
from company_sim.utils import discord_logger
from typing import Tuple, Any
load_dotenv()
# model = os.getenv("MODEL")
gemini_llm = LLM(     model=os.getenv("MODEL_NAME"), base_url=os.getenv("BASE_URL"), api_key=os.getenv("CUSTOM_API_KEY"), temperature=0 )



def _step_callback(output) -> None:
    """Callback dopo ogni step dell'agente - aspetta 10 secondi per diminuire rate limiting"""
    time.sleep(3)

@CrewBase
class DevCrew:
    """Development department crew"""

    @agent
    def dev_manager(self) -> Agent:
        return Agent(
            config=self.agents_config["dev_manager"],
            tools=[read_discord_messages,
                   send_discord_webhook],
            verbose=True,
            step_callback=_step_callback,
            llm= gemini_llm
        )

    @agent
    def dev_junior(self) -> Agent:
        return Agent(
            config=self.agents_config["dev_junior"],
            tools=[read_discord_messages,
                   send_discord_webhook],
            verbose=True,
            reasoning= True,
            step_callback=_step_callback,
            llm= gemini_llm

        )

    @task
    def devman_reply(self) -> Task:
        return Task(
            config=self.tasks_config["dev_manager_reply"],
           # callback = discord_logger.task_callback
        )

    @task
    def devjun_reply(self) -> Task:
        return Task(
            config=self.tasks_config["dev_junior_reply"],
           # callback = discord_logger.task_callback
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.dev_manager(),
                self.dev_junior()
            ],
            tasks=[
                self.devman_reply(),
                self.devjun_reply()
            ],
            process=Process.sequential,
            cache = False,
            verbose=True
        )
