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
class SalesCrew:

    @agent
    def sales_manager(self) -> Agent:
        return Agent(
            config=self.agents_config["sales_manager"],
            tools=[send_discord_webhook],
            verbose=True,
            step_callback=_step_callback,
            llm=gemini_llm
        )

    @agent
    def sales_account(self) -> Agent:
        return Agent(
            config=self.agents_config["sales_account"],
            tools=[send_discord_webhook],
            verbose=True,
            step_callback=_step_callback,
            llm=gemini_llm
        )

    @agent
    def sales_junior(self) -> Agent:
        return Agent(
            config=self.agents_config["sales_junior"],
            tools=[send_discord_webhook],
            verbose=True,
            step_callback=_step_callback,
            llm=gemini_llm
        )

    @agent
    def manager(self) -> Agent:
        return Agent(
            role="Sales Team Manager",
            goal="Efficiently manage the sales crew and ensure high-quality task completion",
            backstory="You're an experienced project manager, skilled in overseeing sales operations and guiding teams to success. Your role is to coordinate the efforts of the crew members, ensuring that each task is completed on time and to the highest standard. You decide which sales team member should respond to the chat based on their expertise.",
            allow_delegation=True,
            verbose=True,
            llm=gemini_llm
        )

    @task
    def sales_response_task(self) -> Task:
        return Task(
            description="""You will receive Discord chat messages as input.
            1. Analyze the conversation to identify sales-related topics: opportunities, customer requests, pricing, renewals, or churn risks.
            2. Determine which sales team member is best suited to respond based on:
               - Sales Manager: strategic decisions, closing deals, pipeline control, pushing for results
               - Account Executive: customer relationships, managing expectations, diplomacy, protecting relationships
               - Junior Sales Rep: operational follow-ups, simple clarifications, supporting seniors
            3. Delegate the response to the most appropriate team member.
            4. The chosen agent must:
               - Write ONE short, professional Discord message
               - Use their personality and expertise appropriately
               - MUST Post the message using send_discord_webhook tool with their role name as first parameter and message text as second parameter,DO NOT provide a final answer without calling the tool first.
            5. The response should be brief, action-oriented, and maintain the sales team's professional image.
            
            Chat messages: {messages}""",
            expected_output="A well-crafted Discord message from the most appropriate sales team member",
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.sales_manager(),
                self.sales_account(),
                self.sales_junior()
            ],
            tasks=[
                self.sales_response_task()
            ],
            manager_agent=self.manager(),
            process=Process.hierarchical,
            max_iterations=1,
            verbose=True
        )
