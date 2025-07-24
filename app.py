from langchain_community.chat_models import ChatOllama
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage
import json
import re

class DescriptionGenerator:
    def __init__(self, model_name: str = "llama3:latest", base_url: str = "http://localhost:11434"):
        self.llm = ChatOllama(
            model=model_name,
            base_url=base_url
        )
        self.prompt_template = PromptTemplate(
            input_variables=["designation", "yoe", "skills", "extraInfo"],
            template="""Generate a detailed job description for a {designation} with {yoe} years of experience and skills: {skills}. If provided use this additional information: {extraInfo} to provide a more contextual description. If the skills list is empty, use the designation to infer relevant skills.

Return ONLY a valid JSON object in this exact format (no additional text or explanation):

{{
  "designation": "{designation}",
  "experience": {yoe},
  "skills": {skills},
  "description": "Brief job description paragraph (2-3 sentences)",
  "responsibilities": [
    "Responsibility 1",
    "Responsibility 2", 
    "Responsibility 3"
  ],
  "requirements": [
    "Requirement 1",
    "Requirement 2",
    "Requirement 3"
  ]
}}

Generate 3 variations of the job description, each with different wording but similar content. You may increase the content length if necessary, but ensure it remains concise and relevant to the job role. Only return the JSON objects in array format without any additional text or explanation. Do not include any markdown formatting, asterisks, or extra characters in the response. The JSON should be well-structured and easy to parse."""
        )

    def generate_description(self, designation: str, yoe: int, skills: list, extrainfo: str) -> list:
        # Clean up skills - remove empty strings
        cleaned_skills = [skill.strip() for skill in skills if skill.strip()]
        
        # If no valid skills, use empty list
        if not cleaned_skills:
            skills_json = "[]"
        else:
            skills_json = json.dumps(cleaned_skills)
            
        prompt = self.prompt_template.format(
            designation=designation.lower(), 
            yoe=yoe, 
            skills=skills_json,
            extraInfo=extrainfo
        )
        response = self.llm([HumanMessage(content=prompt)])
        
        # print("Raw response:")
        # print(f"'{response.content}'")
        # print(f"Response length: {len(response.content)}")
        # print("\n" + "="*50 + "\n")
        
        try:
            # Try to parse the response as JSON
            result = json.loads(response.content)
            
            # If it's an array, return it as-is
            if isinstance(result, list):
                return result
            # If it's a single object, wrap it in an array for consistency
            elif isinstance(result, dict):
                return [result]
            else:
                raise ValueError("Unexpected response format")
                
        except (json.JSONDecodeError, ValueError) as e:
            print(f"JSON parsing failed: {e}")
            # Fallback: return an array with a single fallback object
            return [{
                "designation": designation.lower(),
                "experience": yoe,
                "skills": cleaned_skills,
                "description": "Failed to generate description",
                "responsibilities": [],
                "requirements": []
            }]
    
# Example usage
if __name__ == "__main__":
    generator = DescriptionGenerator()
    designation = "Project Manager/Technical Lead"
    yoe = 5
    skills = ["MERN", "TypeScript", "MEAN"]
    extraInfo = "Experience with web based applications, familiarity with Agile methodologies, and strong communication skills."

    result = generator.generate_description(designation, yoe, skills, extraInfo)
    print(json.dumps(result, indent=2))