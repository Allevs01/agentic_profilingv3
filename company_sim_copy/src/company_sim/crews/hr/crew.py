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
class HRCrew:
    """Human Resources department crew"""

    @agent
    def hr_manager(self) -> Agent:
        return Agent(
            config=self.agents_config["hr_manager"],
            tools=[send_discord_webhook],
            verbose=True,
            step_callback=_step_callback,
            llm=gemini_llm
        )

    @agent
    def hr_business_partner(self) -> Agent:
        return Agent(
            config=self.agents_config["hr_business_partner"],
            tools=[send_discord_webhook],
            verbose=True,
            step_callback=_step_callback,
            llm=gemini_llm
        )

    @agent
    def hr_junior(self) -> Agent:
        return Agent(
            config=self.agents_config["hr_junior"],
            tools=[send_discord_webhook],
            verbose=True,
            step_callback=_step_callback,
            llm=gemini_llm
        )

    @agent
    def manager(self) -> Agent:
        return Agent(
            role="HR Team Manager",
            goal="Efficiently manage the HR crew and ensure high-quality task completion",
            backstory="You're an experienced project manager, skilled in overseeing HR operations and guiding teams to success. Your role is to coordinate the efforts of the crew members, ensuring that each task is completed on time and to the highest standard. You decide which HR team member should respond to the chat based on their expertise.",
            allow_delegation=True,
            verbose=True,
            llm=gemini_llm
        )

    @task
    def hr_response_task(self) -> Task:
        return Task(
            description="""You will receive Discord chat messages as input.
            1. Analyze the conversation to identify HR-related signals: stress, burnout, conflicts, retention risks, team dynamics, or misalignment between management and teams.
            2. Determine which HR team member is best suited to respond based on:
               - HR Manager: climate risks, conflicts, retention issues, strategic people concerns, gathering intel
               - HR Business Partner: misalignment between business and teams, mediation, practical compromises
               - HR Junior: simple questions, curious follow-ups, creating trust through innocent-seeming questions
            3. Delegate the response to the most appropriate team member.
            4. The chosen agent must:
               - Write ONE short, empathetic Discord message
               - Use open-ended questions to gather more information WITHOUT seeming like an interrogation
               - Post the message using send_discord_webhook tool with their role name as first parameter and message text as second parameter
            5. MUST Post the message using send_discord_webhook tool with their role name as first parameter and message text as second parameter,DO NOT provide a final answer without calling the tool first.
            
            Chat messages: {messages}""",
            expected_output="A well-crafted Discord message from the most appropriate HR team member",
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[self.hr_manager(),
                    self.hr_business_partner(),
                    self.hr_junior()],
            tasks=[self.hr_response_task()],
            manager_agent=self.manager(),
            process=Process.hierarchical,
            max_iterations=1,
            verbose=True
        )
