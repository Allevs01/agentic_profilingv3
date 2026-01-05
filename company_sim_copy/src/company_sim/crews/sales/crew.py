import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, task, crew
from company_sim.tools.discord_tools import (
    read_discord_messages
)
from company_sim.utils import discord_logger

@CrewBase
class SalesCrew:

    @agent
    def sales_manager(self) -> Agent:
        return Agent(
            config=self.agents_config["sales_manager"],
            tools=[read_discord_messages],
            allow_delegation=True,
            verbose=True
        )

    @agent 
    def discord_reader(self) -> Agent:
        return Agent(
            role= "Discord Reader",
            goal="Leggere i messaggi dal canale Discord e sintetizzarli",
            backstory="Un bot che osserva la chat aziendale",
            verbose=True
        )

    @agent
    def sales_junior(self) -> Agent:
        return Agent(
            config=self.agents_config["sales_junior"],
            tools=[read_discord_messages],
            verbose=True
        )


    @agent
    def sales_account(self) -> Agent:
        return Agent(
            config=self.agents_config["sales_account"],
            tools=[read_discord_messages],
            verbose=True
        )

    @task
    def read_task(self) -> Task:
        return Task(
                
            description="""
            Leggi gli ultimi messaggi dal canale Discord.
            Produci un riassunto strutturato con:
            - autore
            - contenuto
            - tono (neutro, sospetto, ostile)
            """,
            agent=self.discord_reader(),
            expected_output="Testo strutturato con i messaggi rilevanti"
    )

    @task
    def sales_reply(self) -> Task:
        return Task(
            config=self.tasks_config["sales_reply"],
            callback = discord_logger.task_callback
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.sales_junior(),
                self.sales_account()
            ],
            tasks=[self.sales_reply()],
            process=Process.hierarchical,
            manager_agent=self.sales_manager(),
            manager_llm=os.getenv("MODEL"),
            planning=False,
            verbose=True
        )
