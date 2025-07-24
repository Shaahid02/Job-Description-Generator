# Job Description Generator API

A FastAPI-based REST API that generates detailed job descriptions using AI (Ollama + LangChain).

## Features

- 🚀 Fast and modern API built with FastAPI
- 🤖 AI-powered job description generation
- 📝 Generates 3 variations of job descriptions
- 🔧 Handles empty skills (auto-infers from job title)
- 📊 Automatic API documentation
- ✅ Input validation and error handling
- 🌐 CORS support for frontend integration

## Setup

### 1. Install Dependencies

```bash
# Install venv using python first
python -m venv venv

# Activate your virtual environment
.\venv\Scripts\Activate.ps1

# Install required packages
pip install -r requirements.txt
```

### 2. Ensure Ollama is Running

Make sure you have Ollama installed and the `llama3:latest` model is available:

```bash
# Check if Ollama is running
ollama list

# If llama3 is not available, pull it
ollama pull llama3:latest
```

### 3. Start the API Server

```bash
# Start the development server
uvicorn api:app --reload

# Or run directly
python api.py
```

The API will be available at: `http://localhost:8000`

## API Documentation

Once the server is running, you can access:

- **Interactive API docs (Swagger UI)**: http://localhost:8000/docs
- **Alternative docs (ReDoc)**: http://localhost:8000/redoc

## API Endpoints

### `GET /health`

Health check endpoint to verify API status.

**Response:**

```json
{
  "status": "healthy",
  "service": "Job Description Generator API",
  "generator_status": "initialized",
  "message": "API is running successfully"
}
```

### `POST /generate-job-description`

Generate job descriptions based on input parameters.

**Request Body:**

```json
{
  "designation": "Software Engineer",
  "yoe": 5,
  "skills": ["Python", "Django", "React"],
  "extraInfo": "Experience with web-based applications"
}
```

**Response:**

```json
{
  "success": true,
  "data": [
    {
      "designation": "software engineer",
      "experience": 5,
      "skills": ["Python", "Django", "React"],
      "description": "We are seeking a skilled Software Engineer...",
      "responsibilities": [
        "Design and develop web applications",
        "Collaborate with cross-functional teams",
        "Write clean, maintainable code"
      ],
      "requirements": [
        "5+ years of software development experience",
        "Proficiency in Python and Django",
        "Experience with React framework"
      ]
    }
    // ... 2 more variations
  ],
  "message": "Successfully generated 3 job description variations",
  "count": 3
}
```

### `GET /example`

Get an example request body for testing.

### `GET /designations`

Get a list of commonly supported job designations.

## Usage Examples

### Using curl

```bash
# Health check
curl -X GET "http://localhost:8000/health"

# Generate job descriptions
curl -X POST "http://localhost:8000/generate-job-description" \
  -H "Content-Type: application/json" \
  -d '{
    "designation": "Data Scientist",
    "yoe": 3,
    "skills": ["Python", "Machine Learning", "SQL"],
    "extraInfo": "Experience with ML pipelines and data visualization"
  }'
```

### Using Python requests

```python
import requests

response = requests.post(
    "http://localhost:8000/generate-job-description",
    json={
        "designation": "Frontend Developer",
        "yoe": 4,
        "skills": ["React", "TypeScript", "CSS"],
        "extraInfo": "Experience with modern frontend frameworks"
    }
)

result = response.json()
print(f"Generated {result['count']} job descriptions")
```

### Using JavaScript/Fetch

```javascript
fetch("http://localhost:8000/generate-job-description", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    designation: "DevOps Engineer",
    yoe: 6,
    skills: ["Docker", "Kubernetes", "AWS"],
    extraInfo: "Experience with CI/CD pipelines",
  }),
})
  .then((response) => response.json())
  .then((data) => console.log(data));
```

## Testing

Run the test script to verify the API is working:

```bash
# Make sure the API is running first
python test_api.py
```

## Error Handling

The API includes comprehensive error handling:

- **400 Bad Request**: Invalid input data
- **500 Internal Server Error**: AI generation failures or server issues

Example error response:

```json
{
  "success": false,
  "message": "Designation cannot be empty",
  "error": "Invalid input: designation is required"
}
```

## Production Deployment

For production deployment:

1. Set proper CORS origins in `api.py`
2. Use environment variables for configuration
3. Deploy to cloud platforms (Heroku, AWS, etc.)
4. Use a production WSGI server like Gunicorn

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker api:app
```

## File Structure

```
Job Description Generator/
├── app.py                 # Core job description generator class
├── api.py                 # FastAPI application
├── test_api.py           # API testing script
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── venv/                # Virtual environment
```

## Dependencies

- **fastapi**: Modern web framework for APIs
- **uvicorn**: ASGI server for FastAPI
- **pydantic**: Data validation and parsing
- **langchain**: AI/LLM framework
- **langchain_community**: Community LangChain components

## Troubleshooting

### Common Issues

1. **"Import fastapi could not be resolved"**

   - Solution: Install dependencies with `pip install -r requirements.txt`

2. **"Connection refused" when testing**

   - Solution: Make sure the API server is running with `uvicorn api:app --reload`

3. **"Generator initialization failed"**

   - Solution: Ensure Ollama is running and `llama3:latest` model is available

4. **"JSON parsing failed" errors**
   - Solution: Check that the LLM model is working properly by testing `app.py` directly

### Debug Mode

To enable debug output, uncomment the print statements in `app.py`:

```python
# In app.py, uncomment these lines:
print("Raw response:")
print(f"'{response.content}'")
print(f"Response length: {len(response.content)}")
print("\n" + "="*50 + "\n")
```
