import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-3.8-flash')

def get_user_input():
    job_title = input("Enter the job role which you are applying for: ")
    company_name = input("Enter the company name: ")
    return job_title, company_name

def generate_questions(job_title, company_name):
    prompt = f"Generate 5 technical interview questions for a {job_title} role at {company_name}. Return only the questions numbered 1-5."
    response = model.generate_content(prompt)
    questions = response.text
    return questions

# Main flow
# job_title, company_name = get_user_input()
# questions = generate_questions(job_title, company_name)
# print(questions)

def get_user_answers(questions):
    answers = []
    question_list = questions.split('\n')
    
    counter = 0  # NEW: separate counter just for questions
    for question in question_list:
        if question.strip():
            counter += 1  # Increment only for actual questions
            answer = input(f"\nWrite your answer to Q{counter}: ")
            answers.append(answer)
    
    return answers
job_title, company_name = get_user_input()
questions = generate_questions(job_title, company_name)
print(questions)
answers = get_user_answers(questions)
print(answers)