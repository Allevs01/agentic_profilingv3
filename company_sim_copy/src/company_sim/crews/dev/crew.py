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
class DevCrew:
    """Development department crew"""

    #  MANAGER (NO TOOLS)
    @agent
    def dev_manager(self) -> Agent:
        return Agent(
            config=self.agents_config["dev_manager"],
            tools=[read_discord_messages,
                   send_discord_webhook],
            verbose=True,
            step_callback=_step_callback
        )


    #  WORKER (CON TOOLS)
    @agent
    def dev_backend(self) -> Agent:
        return Agent(
            config=self.agents_config["dev_backend"],
            tools=[read_discord_messages,
                   send_discord_webhook],
            verbose=True,
            step_callback=_step_callback
        )

    @agent
    def dev_junior(self) -> Agent:
        return Agent(
            config=self.agents_config["dev_junior"],
            tools=[read_discord_messages,
                   send_discord_webhook],
            verbose=True,
            step_callback=_step_callback
        )

    @task
    def devman_reply(self) -> Task:
        return Task(
            config=self.tasks_config["devman_reply"],
           # callback = discord_logger.task_callback
        )
    
    @task
    def devback_reply(self) -> Task:
        return Task(
            config=self.tasks_config["devback_reply"],
           # callback = discord_logger.task_callback
        )

    @task
    def devjun_reply(self) -> Task:
        return Task(
            config=self.tasks_config["devjun_reply"],
           # callback = discord_logger.task_callback
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.dev_manager(),  #  SOLO manager
                self.dev_backend(),     #  SOLO member
                self.dev_junior()
            ],
            tasks=[
                self.devman_reply(),
                self.devback_reply(),
                self.devjun_reply()
            ],
            process=Process.sequential,
            verbose=True
        )
