import os
from dotenv import load_dotenv
import time
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, task, crew, before_kickoff
from company_sim.tools.discord_tools import (
    read_discord_messages,
    send_discord_webhook
)
from company_sim.utils import discord_logger
load_dotenv()
# model = os.getenv("MODEL")
gemini_llm = LLM(     model=os.getenv("MODEL_NAME"), base_url=os.getenv("BASE_URL"), api_key=os.getenv("CUSTOM_API_KEY") )


def _step_callback(output) -> None:
    """Callback dopo ogni step dell'agente - aspetta 10 secondi per diminuire rate limiting"""
    time.sleep(1)

@CrewBase
class DevCrew:
    """Development department crew"""

    @agent
    def dev_manager(self) -> Agent:
        return Agent(
            config=self.agents_config["dev_manager"],
            tools=[send_discord_webhook],
            verbose=True,
            step_callback=_step_callback,
            llm= gemini_llm
        )

    @agent
    def dev_backend(self) -> Agent:
        return Agent(
            config=self.agents_config["dev_backend"],
            tools=[send_discord_webhook],
            verbose=True,
            step_callback=_step_callback,
            llm= gemini_llm

        )

    @agent
    def dev_junior(self) -> Agent:
        return Agent(
            config=self.agents_config["dev_junior"],
            tools=[send_discord_webhook],
            verbose=True,
            step_callback=_step_callback,
            llm= gemini_llm

        )

    @agent
    def manager(self) -> Agent:
        return Agent(
            role="Development Team Manager",
            goal="Efficiently manage the dev crew and ensure high-quality task completion",
            backstory="You're an experienced project manager, skilled in overseeing development projects and guiding teams to success. Your role is to coordinate the efforts of the crew members, ensuring that each task is completed on time and to the highest standard. You decide which developer should respond to the chat based on their expertise.",
            allow_delegation=True,
            verbose=True,
            llm=gemini_llm
        )

    @task
    def dev_response_task(self) -> Task:
        return Task(
            description="""You will receive Discord chat messages as input.
            1. Analyze the conversation to identify development-related topics: bugs, features, technical architecture, performance, security, or technical debt.
            2. Determine which developer is best suited to respond based on:
               - Senior Software Engineer: architecture decisions, legacy code, technical quality, complex problems, defensive about past choices
               - Backend Developer: API issues, database problems, performance, scalability, concrete technical solutions
               - Junior Developer: simple tasks, operational support, learning opportunities, low-risk changes
            3. Delegate the response to the most appropriate team member.
            4. The chosen agent must:
               - Write ONE short, technical Discord message
               - Use their personality and technical expertise appropriately
               - MUST Post the message using send_discord_webhook tool with their role name as first parameter and message text as second parameter,DO NOT provide a final answer without calling the tool first.
            5. The response should be technically accurate, pragmatic, and protect code quality.
            
            Chat messages: {messages}""",
            expected_output="A well-crafted Discord message from the most appropriate developer",
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.dev_manager(),
                self.dev_backend(),
                self.dev_junior()
            ],
            tasks=[
                self.dev_response_task()
            ],
            manager_agent=self.manager(),
            manager_llm=gemini_llm,
            process=Process.hierarchical,
            max_iterations=1,
            verbose=True
        )
