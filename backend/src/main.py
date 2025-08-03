from groq import Groq
from fastapi import FastAPI, cli
from dotenv import load_dotenv
import os
import json
from fastapi.middleware.cors import CORSMiddleware


load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or restrict to ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm = Groq(api_key=os.getenv("GROK_API_KEY"))


def challenge_ai_gen() -> dict:
    
    system_prompt = """You are an expert coding challenge creator. 
    Your task is to generate a coding question with multiple choice answers.
    The question should be appropriate for the specified difficulty level.

    For easy questions: Focus on basic syntax, simple operations, or common programming concepts.
    For medium questions: Cover intermediate concepts like data structures, algorithms, or language features.
    For hard questions: Include advanced topics, design patterns, optimization techniques, or complex algorithms.

    Return the challenge in the following JSON structure:
    {
        "title": "The question title",
        "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
        "correct_answer_id": 0, // Index of the correct answer (0-3)
        "explanation": "Detailed explanation of why the correct answer is right"
    }

    Make sure the options are plausible but with only one clearly correct answer.
    """
    try:
        response = llm.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Changed to a generative model
            messages=[
                {"role": "user", "content": system_prompt + "\nGenerate a medium difficulty coding question."}
            ],
            response_format={"type": "json_object"},
            temperature=0.7,
            max_tokens=512,
            top_p=1,
            stream=False,
        )
        content = response.choices[0].message.content
        challenge = json.loads(content)

        required_fields = ["title", "options", "correct_answer_id", "explanation"]
        for field in required_fields:
            if field not in challenge:
                raise ValueError(f"Missing required field: {field}")


        return challenge
    except Exception as e:
        print(f"Error generating challenge: {e}")
        return {
            "title": "Error generating challenge",
            "options": ["Please try again later"],
            "correct_answer_id": 0,
            "explanation": str(e)
        }


@app.get("/generate-challenge")
async def generate_challenge():
    """
    Endpoint to generate a coding challenge.
    Returns a JSON object with the challenge details.
    """
    challenge = challenge_ai_gen()
    return challenge

