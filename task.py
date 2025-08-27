## Importing libraries and files
from crewai import Task
from agents import financial_analyst, document_verifier, investment_advisor, risk_assessor
from tools import read_financial_document, search_tool

# Main Financial Document Analysis Task
analyze_financial_document_task = Task(
    description="""
    Conduct a comprehensive analysis of the uploaded financial document based on the user query: {query}
    
    Your analysis should include:
    1. Extract and read the financial document thoroughly
    2. Identify key financial metrics (revenue, profit margins, debt ratios, cash flow)
    3. Analyze financial performance trends and patterns
    4. Compare metrics to industry standards where applicable
    5. Provide data-driven insights based on the document content
    6. Address the specific user query with factual information
    
    Use the financial document reading tool to access the actual document content.
    Base all analysis on factual data from the document.
    """,
    expected_output="""
    A comprehensive financial analysis report containing:
    - Executive summary of key findings
    - Financial metrics analysis (with specific numbers from the document)
    - Performance trends and insights
    - Strengths and areas of concern identified
    - Professional recommendations based on the analysis
    - Direct answers to the user's specific query: {query}
    
    Format: Professional report with clear sections and bullet points where appropriate.
    """,
    agent=financial_analyst,
    #tools=[read_financial_document, search_tool]
)

# Document Verification Task
document_verification_task = Task(
    description="""
    Verify the financial document and ensure it contains valid financial information:
    
    1. Confirm the document can be read and processed
    2. Identify the type of financial document (10-K, 10-Q, earnings report, etc.)
    3. Extract basic company information and reporting period
    4. Verify presence of key financial statements or sections
    5. Flag any data quality issues or missing information
    """,
    expected_output="""
    Document verification report including:
    - Document type and format confirmation
    - Company name and reporting period
    - Key sections identified in the document
    - Data quality assessment
    - Any issues or limitations found
    
    Format: Structured verification checklist with clear status indicators.
    """,
    agent=document_verifier,
    #tools=[read_financial_document]
)

# Investment Analysis Task
investment_analysis_task = Task(
    description="""
    Based on the financial document analysis, provide investment insights for the query: {query}
    
    Your analysis should:
    1. Evaluate the company's financial health and performance
    2. Identify key investment strengths and risks
    3. Assess growth potential and market position
    4. Consider valuation metrics if available
    5. Provide balanced investment perspective
    6. Include relevant market context and comparisons
    """,
    expected_output="""
    Investment analysis report containing:
    - Investment thesis summary
    - Key financial strengths and weaknesses
    - Growth opportunities and risks
    - Valuation assessment (if data available)
    - Market context and competitive position
    - Balanced investment recommendation with rationale
    
    Format: Professional investment memo with clear reasoning and data support.
    """,
    agent=investment_advisor,
    #tools=[search_tool]
)

# Risk Assessment Task
risk_assessment_task = Task(
    description="""
    Conduct comprehensive risk analysis based on the financial document and query: {query}
    
    Analyze:
    1. Financial risks (liquidity, solvency, profitability)
    2. Operational risks identified in the document
    3. Market and industry risks
    4. Regulatory and compliance considerations
    5. Risk mitigation strategies
    6. Overall risk rating and explanation
    """,
    expected_output="""
    Risk assessment report including:
    - Executive risk summary with overall risk rating
    - Detailed risk analysis by category:
      * Financial risks
      * Operational risks  
      * Market risks
      * Regulatory risks
    - Risk mitigation recommendations
    - Key risk indicators to monitor
    
    Format: Structured risk report with clear risk levels and actionable recommendations.
    """,
    agent=risk_assessor,
    #tools=[read_financial_document, search_tool]
)
