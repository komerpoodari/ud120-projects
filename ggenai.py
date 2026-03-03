from google import genai
from dotenv import load_dotenv
from google.genai import types
import os

# Initialize Client - Ensure GEMINI_API_KEY is in your environment variables
# Best practice: Load from a secure source, not hardcoded
load_dotenv()  # Load environment variables from a .env file if using python-dotenv
api_key = os.getenv("GEMINI_API_KEY") # Ensure this environment variable is set before running the script
print(f"Using API Key: {api_key[:4]}...")  # Print only the first few characters for verification

client = genai.Client(api_key=api_key)


# 1. TOOL DEFINITION: Enabling Google Search for the Researcher
search_tool = types.Tool(
    google_search=types.GoogleSearch()
)

def run_agentic_workflow():
    print("--- STARTING AGENTIC WORKFLOW ---")

    # PHASE 1: THE RESEARCHER (The 'Producer')
    # We give it broad freedom with guided focus areas.
    researcher_instruction = """You are an Elite Cybersecurity Intelligence Researcher. 
    Your mission is to discover and prioritize AI security 'horror stories' from the last 7 days.
    
    FOCUS AREAS (Not exhaustive):
    - IAM/Access Control failures in Agentic frameworks.
    - OpenClaw or related open-source vulnerabilities.
    - Socio-technical horrors (AI-motivated incidents, deepfake fraud).
    - 'Agency Abuse' where agents execute unauthorized destructive actions.
    - Cyber-physical systems safety and security incidents (e.g., autonomous vehicles, industrial control systems).
    
    FREEDOM MANDATE: If you find a novel threat outside these categories that poses 
    a high risk to Cyber-Physical Systems (CPS) or enterprise integrity, prioritize it.
    """

    researcher_config = types.GenerateContentConfig(
        tools=[search_tool],
        system_instruction=researcher_instruction,
        temperature=1.0 # Higher temperature allows for better 'discovery'
    )

    print("[Agent 1] Researcher: Scouring the web for the latest threats...")
    research_query = "Summarize the top 5 AI security/safety horror stories from the last week. Provide links."
    
    research_response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=research_query,
        config=researcher_config
    )
    
    raw_intelligence = research_response.text
    print(f"[Agent 1] Researcher: Triage complete. Identified {len(raw_intelligence.split())} words of data.")

    # --- THE PIPE: Data passes from Researcher to Reporter ---

    # PHASE 2: THE REPORTER (The 'Consumer')
    # Its job is structure, clarity, and executive communication.
    reporter_instruction = """You are a Senior Security Communications Officer. 
    Take the provided raw intelligence and transform it into a professional Markdown report.
    
    STRUCTURE:
    1. Executive Summary: 2-3 sentences on the 'State of the Week'.
    2. Threat Table: [Priority | Incident | Recommended Control/Guardrail].
    3. Detailed Analysis: A brief paragraph for each story with resource links.
    
    AUDIENCE: CISSP-level professionals and Automotive Security Engineers."""

    reporter_config = types.GenerateContentConfig(
        system_instruction=reporter_instruction,
        temperature=0.1 # Low temperature for consistent, structured formatting
    )

    print("[Agent 2] Reporter: Generating Weekly Threat Brief...")
    
    report_response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"Please format the following research data into a report: {raw_intelligence}",
        config=reporter_config
    )

    # 3. OUTPUT: Saving the results to your sandbox
    filename = "Weekly_AI_Threat_Brief.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(report_response.text)

    print(f"--- WORKFLOW COMPLETE ---")
    print(f"Report successfully generated: {os.path.abspath(filename)}")

if __name__ == "__main__":
    try:
        run_agentic_workflow()
    except Exception as e:
        print(f"Workflow failed: {e}")