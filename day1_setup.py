"""
AI Interview Prep - Day 1: Gemini API Test
This script tests that your Gemini API connection works
"""

import os
from dotenv import load_dotenv
from google import genai
from google.genai import errors

MODEL_NAME = "gemini-3.8-flash"
REQUEST_TIMEOUT_MS = 60_000

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv('GEMINI_API_KEY')

if not API_KEY:
    print("ERROR: API key not found in .env file!")
    exit()

# Configure the supported Gemini client with a bounded request time.
client = genai.Client(
    api_key=API_KEY,
    http_options={"timeout": REQUEST_TIMEOUT_MS},
)

def test_api_call(prompt):
    """Make a single API call to Gemini"""
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )
        return response.text or "Error: Gemini returned an empty response."
    except errors.ClientError as error:
        if error.code == 429:
            return "Error: Gemini request quota reached. Wait for the retry window or check your plan and billing."
        return f"Error: Gemini rejected the request ({error.code}): {error.message or error.status}"
    except errors.APIError as error:
        return f"Error: Gemini service error ({error.code}): {error.message or error.status}"
    except TimeoutError:
        return "Error: Gemini request timed out after 60 seconds. Check your network and try again."
    except Exception as e:
        return f"Error: {str(e)}"

# Test 1: Simple greeting
print("=" * 50)
print("TEST 1: Simple greeting")
print("=" * 50)
response1 = test_api_call("Say hello to Vinay in one sentence")
print(response1)
print("\n")

# Test 2: Generate interview question
print("=" * 50)
print("TEST 2: Generate interview question")
print("=" * 50)
response2 = test_api_call("Generate one technical interview question for a Python Backend Developer role")
print(response2)
print("\n")

# Test 3: Evaluate an answer
print("=" * 50)
print("TEST 3: Evaluate an answer")
print("=" * 50)
question = "What is the difference between lists and tuples in Python?"
user_answer = "Lists are mutable and tuples are immutable. That means you can change a list after creating it, but you cannot change a tuple."
prompt = f"Question: {question}\nAnswer: {user_answer}\nEvaluate this answer briefly and suggest improvements."
response3 = test_api_call(prompt)
print(response3)
print("\n")

print("=" * 50)
print("All tests completed.")
print("=" * 50)
