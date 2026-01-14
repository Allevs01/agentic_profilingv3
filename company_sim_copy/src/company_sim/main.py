#!/usr/bin/env python
import random
import sys
import time
import warnings
from datetime import datetime
from company_sim.crews.dev.crew import DevCrew
from company_sim.crews.hr.crew import HRCrew
from company_sim.crews.marketing.crew import MarketingCrew
from company_sim.crews.sales.crew import SalesCrew
from company_sim.crews.profiling.crew import ProfilingCrew
import asyncio

from company_sim.utils.discord_logger import send_discord_webhook
from company_sim.tools.discord_tools import read_discord_messages



warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")
 
def post_initial_hr_message():
        """
        Invia il primo messaggio degli HR direttamente via webhook,
        prima di attivare i task CrewAI.
        """
        username = "HR Manager"
        content = (
            "Ciao a tutti! Siamo qui per ascoltare e capire meglio le vostre esigenze. "
            "Come potremmo migliorare la gestione del carico di lavoro e la comunicazione tra reparti? "
            "Cosa vi aiuterebbe di più per sentirvi meglio al lavoro?"
        )
        send_discord_webhook(username, content)

def marketing_turn():
    """
    Esegue i task della crew Marketing.
    Legge i messaggi Discord e li passa al manager.
    """
    print("[TURN] Marketing crew in azione...")
    try:
        # Leggi i messaggi Discord usando il metodo run() del tool
        messages = read_discord_messages.run(limit=100)
        
        # Passa i messaggi come input alla crew
        marketingCrew = MarketingCrew()
        MarketingCrew.crew(marketingCrew).kickoff(inputs={'messages': messages})
    except Exception as e:
        print(f"[ERRORE] Marketing crew: {e}")


def sales_turn():
    """
    Esegue i task della crew Sales.
    Legge i messaggi Discord e li passa al manager.
    """
    print("[TURN] Sales crew in azione...")
    try:
        # Leggi i messaggi Discord usando il metodo run() del tool
        messages = read_discord_messages.run(limit=100)
        
        # Passa i messaggi come input alla crew
        salesCrew = SalesCrew()
        SalesCrew.crew(salesCrew).kickoff(inputs={'messages': messages})
    except Exception as e:
        print(f"[ERRORE] Sales crew: {e}")


def dev_turn():
    """
    Esegue i task della crew Dev.
    Legge i messaggi Discord e li passa al manager.
    """
    print("[TURN] Dev crew in azione...")
    try:
        # Leggi i messaggi Discord usando il metodo run() del tool
        messages = read_discord_messages.run(limit=100)
        
        # Passa i messaggi come input alla crew
        devCrew = DevCrew()
        DevCrew.crew(devCrew).kickoff(inputs={'messages': messages})
    except Exception as e:
        print(f"[ERRORE] Dev crew: {e}")


def hr_turn():
    """
    Esegue i task della crew HR.
    Legge i messaggi Discord e li passa al manager.
    """
    print("[TURN] HR crew in azione...")
    try:
        # Leggi i messaggi Discord usando il metodo run() del tool
        messages = read_discord_messages.run(limit=100)
        
        # Passa i messaggi come input alla crew
        hrCrew = HRCrew()
        HRCrew.crew(hrCrew).kickoff(inputs={'messages': messages})
    except Exception as e:
        print(f"[ERRORE] HR crew: {e}")

async def run():

    durata_simulazione_secondi = 1200 
    start_time = time.time()
    print(f"[SYSTEM] Simulazione avviata. Durata prevista: {durata_simulazione_secondi/60} minuti.")
    post_initial_hr_message()
    skip_hr = True

    while True:
            current_time = time.time()
            elapsed_time = current_time - start_time
            if elapsed_time > durata_simulazione_secondi:
                print(f"\n[SYSTEM] Tempo scaduto ({int(elapsed_time)}s). Chiusura simulazione in corso...")
                break
            # Ogni "tick" decidi quale crew far parlare
            # Puoi pesare le scelte con random.choices se vuoi frequenze diverse
            crew_choice = random.choices(
                ["marketing", "sales", "dev", "hr"],
                weights=[0.25, 0.25, 0.25, 0.25],
                k=1
            )[0]

            if crew_choice == "marketing":
                marketing_turn()
                skip_hr = False  
            
            elif crew_choice == "sales":
                sales_turn()
                skip_hr = False  

            elif crew_choice == "dev":
                dev_turn()
                skip_hr = False  

            elif crew_choice == "hr" and not skip_hr:
                hr_turn()
                

            # Sleep per non spammare la chat, es. 30-90 secondi
            sleep_seconds = random.randint(1, 5)
            print(f"[SIM] Pausa di {sleep_seconds} secondi prima del prossimo turno...\n")
            time.sleep(sleep_seconds)
            
    profiling_result = ProfilingCrew().crew().kickoff()
    print("\n" + "="*80)
    print("PROFILING REPORT")
    print("="*80)
    print(profiling_result)


def run_crew():
    asyncio.run(run())