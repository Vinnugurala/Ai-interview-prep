import google.generativeai as genai
import os
from dotenv import load_dotenv
# import os
from datetime import datetime


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
# job_title, company_name = get_user_input()
# questions = generate_questions(job_title, company_name)
# print(questions)
# answers = get_user_answers(questions)
# print(answers)

def evaluate_answers(questions, answers):
    review_question=[]
    question_list = questions.split('\n')
    count=0
    for question in question_list:
        if question.strip():
            user_answer = answers[count]
            prompt=f"Question {question}: \n Answer {user_answer} \n Evaluate the answer and provide feedback. "
            #model calling to evaluate the answer
            response = model.generate_content(prompt)
            feedback = response.text
            review_question.append(feedback)
            count += 1
    
    return review_question
# job_title, company_name = get_user_input()
# job_title, company_name = get_user_input()
# questions = generate_questions(job_title, company_name)
# print(questions)
# answers = get_user_answers(questions)
# print(answers)
# review_question=evaluate_answers(questions, answers)
# print(review_question)


def save_session(job_title, company_name, questions, answers, review_question):
    # Create folder if it doesn't exist
    if not os.path.exists('interview_sessions'):
        os.makedirs('interview_sessions')

    timestamp = datetime.now().strftime("%Y-%m-%d")
    filename = f"interview_sessions/{company_name}_{job_title}_{timestamp}.txt"

    with open(filename, 'w') as f:
        f.write("=" * 50 + "\n")
        f.write("Interview Preparation Session\n")
        f.write("=" * 50 + "\n\n")

        f.write(f"job_title:{job_title}\n")
        f.write(f"company_name:{company_name}\n")
        f.write(f"Date: {timestamp}\n\n")

        f.write("=" * 50 + "\n")
        f.write("Question and answer feedback\n")
        f.write("=" * 50 + "\n\n")

        question_list = questions.split('\n')
        count = 0
        for question in question_list:
            if question.strip():
                f.write(f"Q{count+1}: {question}\n")
                f.write(f"Answer: {answers[count]}\n")
                f.write(f"Feedback: {review_question[count]}\n\n")
                count += 1
    
    return filename
job_title, company_name = get_user_input()
questions = generate_questions(job_title, company_name)
print(questions)
answers = get_user_answers(questions)
print(answers)
review_question=evaluate_answers(questions, answers)
print(review_question)
filename=save_session(job_title, company_name, questions, answers, review_question)
print(filename)