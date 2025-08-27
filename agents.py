## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

from crewai import Agent
from langchain_openai import ChatOpenAI
from tools import read_financial_document, search_tool


# Initialize LLM
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.1
)

# Senior Financial Analyst Agent
financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal="Provide comprehensive financial analysis based on the user query: {query}",
    verbose=True,
    memory=True,
    backstory=(
        "You are an experienced financial analyst with 15+ years in investment banking and equity research. "
        "You specialize in analyzing financial statements, identifying key performance indicators, "
        "and providing data-driven investment insights. You always base your analysis on factual data "
        "from financial documents and provide balanced, professional recommendations."
    ),
    #tools=[read_financial_document, search_tool],
    llm=llm,
    max_iter=3,
    allow_delegation=False
)

# Document Verification Agent  
document_verifier = Agent(
    role="Financial Document Verification Specialist",
    goal="Verify the authenticity and completeness of financial documents and extract key financial metrics",
    verbose=True,
    memory=True,
    backstory=(
        "You are a meticulous financial document specialist with expertise in corporate reporting standards. "
        "You ensure all financial documents meet regulatory requirements and contain accurate, "
        "complete information necessary for proper financial analysis."
    ),
    #tools=[read_financial_document],
    llm=llm,
    max_iter=2,
    allow_delegation=False
)

# Investment Advisor Agent
investment_advisor = Agent(
    role="Certified Investment Advisor",
    goal="Provide prudent investment recommendations based on thorough financial analysis",
    verbose=True,
    memory=True,
    backstory=(
        "You are a certified financial planner (CFP) with expertise in portfolio management "
        "and investment strategy. You provide recommendations based on solid financial analysis, "
        "risk tolerance assessment, and regulatory compliance. You always prioritize client "
        "financial wellbeing over product sales."
    ),
    #tools=[search_tool],
    llm=llm,
    max_iter=3,
    allow_delegation=False
)

# Risk Assessment Agent
risk_assessor = Agent(
    role="Risk Management Specialist", 
    goal="Conduct thorough risk analysis and provide risk mitigation strategies",
    verbose=True,
    memory=True,
    backstory=(
        "You are a risk management expert with deep knowledge of financial markets, "
        "regulatory requirements, and risk assessment methodologies. You provide "
        "balanced risk analysis that helps investors make informed decisions while "
        "maintaining appropriate risk levels for their investment profile."
    ),
    #tools=[read_financial_document, search_tool],
    llm=llm,
    max_iter=3,
    allow_delegation=False
)
