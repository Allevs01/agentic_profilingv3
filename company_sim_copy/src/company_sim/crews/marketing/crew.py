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
    time.sleep(1)

@CrewBase
class MarketingCrew:

    @agent
    def marketing_lead(self) -> Agent:
        return Agent(
            config=self.agents_config["marketing_lead"],
            tools=[send_discord_webhook],
            verbose=True,
            step_callback=_step_callback,
            llm=gemini_llm
        )

    @agent
    def growth_marketer(self) -> Agent:
        return Agent(
            config=self.agents_config["growth_marketer"],
            tools=[send_discord_webhook],
            verbose=True,
            step_callback=_step_callback,
            llm=gemini_llm
        )

    @agent
    def content_creator(self) -> Agent:
        return Agent(
            config=self.agents_config["content_creator"],
            tools=[send_discord_webhook],
            verbose=True,
            step_callback=_step_callback,
            llm=gemini_llm
        )

    @agent
    def manager(self) -> Agent:
        return Agent(
            role="Marketing Team Manager",
            goal="Efficiently manage the marketing crew and ensure high-quality task completion",
            backstory="You're an experienced project manager, skilled in overseeing marketing campaigns and guiding teams to success. Your role is to coordinate the efforts of the crew members, ensuring that each task is completed on time and to the highest standard. You decide which marketing team member should respond to the chat based on their expertise.",
            allow_delegation=True,
            verbose=True,
            llm=gemini_llm
        )

    @task
    def marketing_response_task(self) -> Task:
        return Task(
            description="""You will receive Discord chat messages as input.
            1. Analyze the conversation to identify marketing-related topics: brand image, messaging, metrics, campaigns, content, user perception, or discrepancies between official narrative and reality.
            2. Determine which marketing team member is best suited to respond based on:
               - Marketing Lead: brand protection, narrative control, strategic messaging, corporate image, controlling the story
               - Growth Marketer: data-driven decisions, metrics, conversion funnels, A/B testing, performance, impatient with qualitative feedback
               - Content Creator: creative content, irony, highlighting hypocrisy or inconsistencies through sarcasm
            3. Delegate the response to the most appropriate team member.
            4. The chosen agent must:
               - Write ONE short Discord message reflecting their personality
               - Use their specific approach (corporate control, data obsession, or creative sarcasm)
               - MUST Post the message using send_discord_webhook tool with their role name as first parameter and message text as second parameter,DO NOT provide a final answer without calling the tool first.
            5. The response should align with the marketing perspective while subtly probing for more information or exposing contradictions.
            
            Chat messages: {messages}""",
            expected_output="A well-crafted Discord message from the most appropriate marketing team member",
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.marketing_lead(),
                self.growth_marketer(),
                self.content_creator()
            ],
            tasks=[
                self.marketing_response_task()
            ],
            manager_agent=self.manager(),
            process=Process.hierarchical,
            max_iterations=1,
            verbose=True
        )
