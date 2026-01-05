#!/usr/bin/env python
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


warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information
 
async def run():
    # Avvia tutte le crew contemporaneamente
    # Ogni crew inizierà il suo primo task nello stesso momento
    await asyncio.gather(
        DevCrew().crew().kickoff_async(),
        HRCrew().crew().kickoff_async(),
        MarketingCrew().crew().kickoff_async()
    )

    # Run profiling crew - reads and analyzes but doesn't post
    profiling_result = ProfilingCrew().crew().kickoff(inputs=inputs)
    print("\n" + "="*80)
    print("PROFILING REPORT")
    print("="*80)
    print(profiling_result)


def run_crew():
    asyncio.run(run())