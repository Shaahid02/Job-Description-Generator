import requests
import json

# Base URL for the API
BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("-" * 50)

def test_job_description_generation():
    """Test job description generation"""
    print("Testing job description generation...")
    
    test_data = {
        "designation": "Software Engineer",
        "yoe": 5,
        "skills": ["Python", "Django", "React"],
        "extraInfo": "Experience with web-based applications and agile methodologies"
    }
    
    response = requests.post(
        f"{BASE_URL}/generate-job-description",
        json=test_data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Success: {result['success']}")
        print(f"Message: {result['message']}")
        print(f"Number of descriptions: {result['count']}")
        print("\nFirst description:")
        if result['data']:
            first_desc = result['data'][0]
            print(f"Designation: {first_desc['designation']}")
            print(f"Experience: {first_desc['experience']}")
            print(f"Skills: {first_desc['skills']}")
            print(f"Description: {first_desc['description'][:100]}...")
    else:
        print(f"Error: {response.text}")
    print("-" * 50)

def test_example_endpoint():
    """Test the example endpoint"""
    print("Testing example endpoint...")
    response = requests.get(f"{BASE_URL}/example")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("-" * 50)

def test_error_handling():
    """Test error handling with invalid data"""
    print("Testing error handling...")
    
    # Test with empty designation
    test_data = {
        "designation": "",
        "yoe": 5,
        "skills": ["Python"],
        "extraInfo": "Test"
    }
    
    response = requests.post(
        f"{BASE_URL}/generate-job-description",
        json=test_data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("-" * 50)

if __name__ == "__main__":
    print("=== Job Description Generator API Test ===\n")
    
    try:
        test_health_check()
        test_example_endpoint()
        test_job_description_generation()
        test_error_handling()
        
        print("All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API.")
        print("Make sure the API is running with: uvicorn api:app --reload")
    except Exception as e:
        print(f"Error during testing: {e}")
