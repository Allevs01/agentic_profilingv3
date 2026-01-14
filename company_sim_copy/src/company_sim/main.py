#!/usr/bin/env python
import random
import sys
import time
import warnings
from datetime import datetime
from company_sim.crews.dev.crew import DevCrew
from company_sim.crews.hr.crew import HRCrew
from company_sim.crews.hr.crew import ProfilingCrew
import asyncio

from company_sim.utils.discord_logger import send_discord_webhook



warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")
 
def post_initial_hr_message():
        """
        Invia il primo messaggio degli HR direttamente via webhook,
        prima di attivare i task CrewAI.
        """
        username = "HR Manager"
        content = (
            "Ciao a tutti! Mi prendo un momento per fare un salto qui nel vostro canale. "
            "So che l'ultimo periodo è stato intenso e volevo semplicemente capire come sta andando la collaborazione e se c'è qualcosa che l'HR può fare per supportarvi meglio nel quotidiano. "
            "Come vi sentite rispetto al lavoro attuale?"
        )
        send_discord_webhook(username, content)

def dev_turn():
    """
    Esegue i task della crew Dev.
    """
    print("[TURN] Dev crew in azione...")
    try:
        devCrew = DevCrew()
        DevCrew.crew(devCrew).kickoff()
    except Exception as e:
        print(f"[ERRORE] Dev crew: {e}")


def hr_turn():
    """
    Esegue i task della crew HR.
    """
    print("[TURN] HR crew in azione...")
    try:
        hrCrew = HRCrew()
        HRCrew.crew(hrCrew).kickoff()
    except Exception as e:
        print(f"[ERRORE] HR crew: {e}")

async def run():

    durata_simulazione_secondi = 600 
    start_time = time.time()
    print(f"[SYSTEM] Simulazione avviata. Durata prevista: {durata_simulazione_secondi/60} minuti.")
    post_initial_hr_message()
   

    while True:
            current_time = time.time()
            elapsed_time = current_time - start_time
            if elapsed_time > durata_simulazione_secondi:
                print(f"\n[SYSTEM] Tempo scaduto ({int(elapsed_time)}s). Chiusura simulazione in corso...")
                break
            dev_turn()
            hr_turn()
            # Sleep per non spammare la chat
            # sleep_seconds = random.randint(5, 10)
            # print(f"[SIM] Pausa di {sleep_seconds} secondi prima del prossimo turno...\n")
            # time.sleep(sleep_seconds)
            
    profiling_result = ProfilingCrew().crew().kickoff()
    print("\n" + "="*80)
    print("PROFILING REPORT")
    print("="*80)
    print(profiling_result)


def run_crew():
    asyncio.run(run())