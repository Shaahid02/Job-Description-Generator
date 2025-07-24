from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import json

print("Importing modules...")

try:
    from app import DescriptionGenerator
    print("Successfully imported DescriptionGenerator")
except Exception as e:
    print(f"Failed to import DescriptionGenerator: {e}")

print("Creating FastAPI app...")

# Initialize FastAPI app
app = FastAPI(
    title="Job Description Generator API",
    description="Generate detailed job descriptions using AI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware to allow requests from frontend applications
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class JobDescriptionRequest(BaseModel):
    designation: str = Field(..., description="Job designation/title", example="Software Engineer")
    yoe: int = Field(..., ge=0, le=50, description="Years of experience", example=5)
    skills: List[str] = Field(default=[], description="List of skills (can be empty)", example=["Python", "Django", "React"])
    extraInfo: Optional[str] = Field(default="", description="Additional context information", example="Experience with web applications")

    class Config:
        json_schema_extra = {
            "example": {
                "designation": "Software Engineer",
                "yoe": 5,
                "skills": ["Python", "Django", "React"],
                "extraInfo": "Experience with web-based applications and agile methodologies"
            }
        }

# Response models
class JobDescription(BaseModel):
    designation: str
    experience: int
    skills: List[str]
    description: str
    responsibilities: List[str]
    requirements: List[str]

class JobDescriptionResponse(BaseModel):
    success: bool
    data: List[JobDescription]
    message: str
    count: int

class ErrorResponse(BaseModel):
    success: bool
    message: str
    error: str

# Initialize the job description generator
print("Initializing DescriptionGenerator...")
try:
    generator = DescriptionGenerator()
    generator_initialized = True
    print("Generator initialized successfully")
except Exception as e:
    generator_initialized = False
    initialization_error = str(e)
    print(f"Generator initialization failed: {e}")

# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint to verify API status
    """
    return {
        "status": "healthy",
        "service": "Job Description Generator API",
        "generator_status": "initialized" if generator_initialized else "failed",
        "message": "API is running successfully" if generator_initialized else f"Generator initialization failed: {initialization_error}"
    }

# Main job description generation endpoint
@app.post(
    "/generate-job-description", 
    response_model=JobDescriptionResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    tags=["Job Description"]
)
async def generate_job_description(request: JobDescriptionRequest):
    """
    Generate job descriptions based on the provided parameters.
    
    Returns an array of 3 different job description variations.
    """
    
    # Check if generator is initialized
    if not generator_initialized:
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "message": "Job description generator is not properly initialized",
                "error": initialization_error
            }
        )
    
    try:
        # Validate input
        if not request.designation.strip():
            raise HTTPException(
                status_code=400,
                detail={
                    "success": False,
                    "message": "Designation cannot be empty",
                    "error": "Invalid input: designation is required"
                }
            )
        
        # Generate job descriptions
        result = generator.generate_description(
            designation=request.designation.strip(),
            yoe=request.yoe,
            skills=request.skills,
            extrainfo=request.extraInfo or ""
        )
        
        # Validate the result
        if not result or not isinstance(result, list):
            raise HTTPException(
                status_code=500,
                detail={
                    "success": False,
                    "message": "Failed to generate job descriptions",
                    "error": "Generator returned invalid result"
                }
            )
        
        # Convert to response format
        job_descriptions = []
        for job_desc in result:
            if isinstance(job_desc, dict):
                job_descriptions.append(JobDescription(**job_desc))
            else:
                # Handle unexpected format
                continue
        
        if not job_descriptions:
            raise HTTPException(
                status_code=500,
                detail={
                    "success": False,
                    "message": "No valid job descriptions were generated",
                    "error": "Generator returned malformed data"
                }
            )
        
        return JobDescriptionResponse(
            success=True,
            data=job_descriptions,
            message=f"Successfully generated {len(job_descriptions)} job description variations",
            count=len(job_descriptions)
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "message": "An unexpected error occurred while generating job descriptions",
                "error": str(e)
            }
        )

# Additional endpoint to get example request
@app.get("/example", tags=["Documentation"])
async def get_example_request():
    """
    Get an example request body for the job description generation
    """
    return {
        "example_request": {
            "designation": "Software Engineer",
            "yoe": 5,
            "skills": ["Python", "Django", "React", "AWS"],
            "extraInfo": "Experience with microservices architecture and agile development"
        },
        "usage": "POST /generate-job-description with the above JSON structure"
    }

# Endpoint to list supported job designations (optional)
@app.get("/designations", tags=["Documentation"])
async def get_supported_designations():
    """
    Get a list of commonly supported job designations
    """
    designations = [
        "Software Engineer",
        "Senior Software Engineer",
        "Full Stack Developer",
        "Frontend Developer",
        "Backend Developer",
        "DevOps Engineer",
        "Data Scientist",
        "Data Engineer",
        "Product Manager",
        "Project Manager",
        "Business Analyst",
        "QA Engineer",
        "Technical Lead",
        "Engineering Manager",
        "UX/UI Designer",
        "System Administrator",
        "Database Administrator",
        "Cybersecurity Specialist"
    ]
    
    return {
        "supported_designations": designations,
        "note": "This API can generate descriptions for any job designation, not limited to this list"
    }

if __name__ == "__main__":
    import uvicorn
    print("Starting server...")
    try:
        uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)
    except Exception as e:
        print(f"Failed to start server: {e}")
        input("Press Enter to exit...")
