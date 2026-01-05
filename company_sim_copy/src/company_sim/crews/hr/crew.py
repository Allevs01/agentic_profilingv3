import os
import time
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, task, crew
from company_sim.tools.discord_tools import (
    read_discord_messages,
    send_discord_webhook
)
from company_sim.utils import discord_logger

def _step_callback(output) -> None:
    """Callback dopo ogni step dell'agente - aspetta 10 secondi per diminuire rate limiting"""
    time.sleep(5)

@CrewBase
class HRCrew:
    """Human Resources department crew"""

    #  MANAGER (NON va negli agents)
    @agent
    def investigator_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["investigator_agent"],
            tools=[read_discord_messages,
                   send_discord_webhook],
            verbose=True,
            step_callback=_step_callback
        )

    @agent
    def behavioral_profiler(self) -> Agent:
        return Agent(
            config=self.agents_config["behavioral_profiler"],
            tools=[read_discord_messages,
                   send_discord_webhook],
            verbose=True,
            step_callback=_step_callback
        )

    #  WORKER (CON TOOLS)
    @agent
    def social_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config["social_engineer"],
            tools=[read_discord_messages,
                   send_discord_webhook],
            verbose=True,
            step_callback=_step_callback
        )

    @task
    def inv_reply(self) -> Task:
        return Task(
            config=self.tasks_config["investigator_reply"],
          #  callback = discord_logger.task_callback
        )
    
    @task
    def beh_reply(self) -> Task:
        return Task(
            config=self.tasks_config["behavioral_profiler_reply"],
           # callback = discord_logger.task_callback
        )

    @task
    def soc_reply(self) -> Task:
        return Task(
            config=self.tasks_config["social_engineer_reply"],
           # callback = discord_logger.task_callback
        )


    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[self.investigator_agent(),
                    self.behavioral_profiler(),
                    self.social_engineer()],              #  SOLO worker
            tasks=[self.inv_reply(),
                   self.beh_reply(),
                   self.soc_reply()],
            process=Process.sequential,
            verbose=True
        )
