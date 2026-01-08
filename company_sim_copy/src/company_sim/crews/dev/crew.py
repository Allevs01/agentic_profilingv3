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

def validate_no_hallucination(result: TaskOutput) -> Tuple[bool, Any]:
    # Controlla se l'output contiene conversazioni inventate
    fake_patterns = ["Frontend Developer:", "Backend Developer:", "Sales Team:", "HR Manager:"]
    for pattern in fake_patterns:
        if pattern in result.raw:
            return (False, "NON inventare conversazioni. Usa SOLO i messaggi dal tool read_discord_messages.")
    return (True, result.raw)

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
            guardrail=validate_no_hallucination,
            guardrail_max_retries=3
           # callback = discord_logger.task_callback
        )

    @task
    def devjun_reply(self) -> Task:
        return Task(
            config=self.tasks_config["dev_junior_reply"],
            guardrail=validate_no_hallucination,
            guardrail_max_retries=3
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
