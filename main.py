from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
import os
import uuid
import asyncio
from typing import Optional

from crewai import Crew, Process
from agents import financial_analyst, document_verifier, investment_advisor, risk_assessor
from task import analyze_financial_document_task, document_verification_task

app = FastAPI(title="Financial Document Analyzer", version="1.0.0")

def run_financial_analysis_crew(query: str, file_path: str = "data/sample.pdf"):
    """
    Run the financial analysis crew with the uploaded document
    
    Args:
        query (str): User's analysis query
        file_path (str): Path to the uploaded financial document
        
    Returns:
        dict: Analysis results from the crew
    """
    try:
        # Create crew with financial analyst and verifier
        financial_crew = Crew(
            agents=[document_verifier, financial_analyst],
            tasks=[document_verification_task, analyze_financial_document_task],
            process=Process.sequential,
            verbose=True
        )
        
        # Execute the crew analysis
        result = financial_crew.kickoff({
            'query': query,
            'file_path': file_path
        })
        
        return {
            "success": True,
            "analysis": str(result),
            "crew_agents": ["document_verifier", "financial_analyst"]
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Crew execution failed: {str(e)}",
            "analysis": None
        }

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Financial Document Analyzer API is running",
        "version": "1.0.0",
        "status": "active"
    }

@app.get("/health")
async def health_check():
    """Detailed health check with system status"""
    return {
        "status": "healthy",
        "api": "operational",
        "endpoints": {
            "analyze": "/analyze - POST endpoint for document analysis",
            "health": "/health - System health check"
        }
    }

@app.post("/analyze")
async def analyze_document(
    file: UploadFile = File(...),
    query: str = Form(default="Provide a comprehensive financial analysis of this document")
):
    """
    Analyze uploaded financial document and provide comprehensive insights
    
    Args:
        file: Uploaded PDF financial document
        query: Specific analysis question or request
        
    Returns:
        JSON response with analysis results
    """
    
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400, 
            detail="Only PDF files are supported for financial document analysis"
        )
    
    # Generate unique file identifier
    file_id = str(uuid.uuid4())
    file_path = f"data/financial_doc_{file_id}.pdf"
    
    try:
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
        
        # Save uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Validate and clean query
        if not query or query.strip() == "":
            query = "Provide a comprehensive financial analysis of this document"
        
        query = query.strip()
        
        # Process the financial document
        analysis_result = run_financial_analysis_crew(
            query=query, 
            file_path=file_path
        )
        
        if analysis_result["success"]:
            return JSONResponse(
                status_code=200,
                content={
                    "status": "success",
                    "query": query,
                    "filename": file.filename,
                    "analysis": analysis_result["analysis"],
                    "agents_used": analysis_result["crew_agents"],
                    "file_id": file_id
                }
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Analysis failed: {analysis_result['error']}"
            )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Unexpected error during document analysis: {str(e)}"
        )
    
    finally:
        # Clean up uploaded file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass  # Ignore cleanup errors

@app.post("/analyze-advanced")
async def analyze_document_advanced(
    file: UploadFile = File(...),
    query: str = Form(default="Provide comprehensive analysis with investment and risk assessment"),
    include_investment_advice: bool = Form(default=True),
    include_risk_assessment: bool = Form(default=True)
):
    """
    Advanced analysis with investment advice and risk assessment
    
    Args:
        file: Uploaded PDF financial document
        query: Specific analysis question
        include_investment_advice: Whether to include investment recommendations
        include_risk_assessment: Whether to include risk analysis
        
    Returns:
        JSON response with comprehensive analysis
    """
    
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400, 
            detail="Only PDF files are supported"
        )
    
    file_id = str(uuid.uuid4())
    file_path = f"data/advanced_analysis_{file_id}.pdf"
    
    try:
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
        
        # Save uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Build crew based on requested analysis
        agents = [document_verifier, financial_analyst]
        tasks = [document_verification_task, analyze_financial_document_task]
        
        if include_investment_advice:
            agents.append(investment_advisor)
            # tasks.append(investment_analysis_task)  # Uncomment when task is ready
            
        if include_risk_assessment:
            agents.append(risk_assessor)
            # tasks.append(risk_assessment_task)  # Uncomment when task is ready
        
        # Create and run comprehensive crew
        comprehensive_crew = Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )
        
        result = comprehensive_crew.kickoff({
            'query': query or "Provide comprehensive financial analysis",
            'file_path': file_path
        })
        
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "query": query,
                "filename": file.filename,
                "analysis_type": "comprehensive",
                "analysis": str(result),
                "agents_used": [agent.role for agent in agents],
                "features": {
                    "investment_advice": include_investment_advice,
                    "risk_assessment": include_risk_assessment
                }
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Advanced analysis failed: {str(e)}"
        )
    
    finally:
        # Clean up uploaded file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
