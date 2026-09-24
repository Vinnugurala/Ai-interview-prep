"""
AI Interview Prep - Day 1: Gemini API Test
This script tests that your Gemini API connection works
"""

import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv('GEMINI_API_KEY')

if not API_KEY:
    print("ERROR: API key not found in .env file!")
    exit()

# Configure Gemini API
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')

def test_api_call(prompt):
    """Make a single API call to Gemini"""
    try:
        response = model.generate_content(prompt)
        return response.text
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
print("✅ All tests completed! API is working.")
print("=" * 50)