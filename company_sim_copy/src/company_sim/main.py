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


warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
       
    }

    try:
        DevCrew().crew().kickoff(inputs=inputs)
        print("⏳ Waiting 10 seconds before next crew...")
        time.sleep(3)
        
        HRCrew().crew().kickoff(inputs=inputs)
        print("⏳ Waiting 10 seconds before next crew...")
        time.sleep(3)
        
        MarketingCrew().crew().kickoff(inputs=inputs)
        print("⏳ Waiting 10 seconds before next crew...")
        time.sleep(3)
        
        # Run profiling crew - reads and analyzes but doesn't post
        profiling_result = ProfilingCrew().crew().kickoff(inputs=inputs)
        print("\n" + "="*80)
        print("PROFILING REPORT")
        print("="*80)
        print(profiling_result)
        
     #   print("⏳ Waiting 10 seconds before next crew...")
     #   time.sleep(10)
     #   SalesCrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(e)
