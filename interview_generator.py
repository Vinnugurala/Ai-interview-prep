import os
from dotenv import load_dotenv
from datetime import datetime
import time
from google import genai
from google.genai import errors

MODEL_NAME = "gemini-3.1-flash-lite"
REQUEST_TIMEOUT_MS = 60_000
MAX_SERVICE_RETRIES = 6
RETRY_BASE_DELAY_SECONDS = 5

# Load API key
load_dotenv()
API_KEY = os.getenv('GEMINI_API_KEY')

if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY is missing. Add it to the .env file before running the app.")

client = genai.Client(
    api_key=API_KEY,
    http_options={"timeout": REQUEST_TIMEOUT_MS},
)


class GeminiGenerationError(Exception):
    """Raised when Gemini cannot generate a response."""


def generate_content(prompt):
    for attempt in range(MAX_SERVICE_RETRIES):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
            )
        except errors.ClientError as error:
            if error.code == 429:
                raise GeminiGenerationError(
                    "Gemini request quota reached. Wait for the retry window or check your plan and billing."
                ) from error
            raise GeminiGenerationError(
                f"Gemini rejected the request ({error.code}): {error.message or error.status}"
            ) from error
        except errors.APIError as error:
            if error.code == 503 and attempt < MAX_SERVICE_RETRIES - 1:
                delay = RETRY_BASE_DELAY_SECONDS * (2**attempt)
                print(f"\nGemini is busy. Retrying in {delay} seconds...")
                time.sleep(delay)
                continue
            raise GeminiGenerationError(
                f"Gemini service error ({error.code}): {error.message or error.status}"
            ) from error
        except TimeoutError as error:
            raise GeminiGenerationError(
                "Gemini request timed out after 60 seconds. Check your network and try again."
            ) from error
        except Exception as error:
            raise GeminiGenerationError(f"Gemini request failed: {error}") from error

        if not response.text:
            raise GeminiGenerationError("Gemini returned an empty response.")

        return response.text


def get_user_input():
    job_title = input("Enter the job role which you are applying for: ").strip()
    company_name = input("Enter the company name: ").strip()
    return job_title, company_name


def generate_questions(job_title, company_name):
    prompt = f"Generate 5 technical interview questions for a {job_title} role at {company_name}. Return only the questions numbered 1-5."
    return generate_content(prompt)


def get_user_answers(questions):
    answers = []
    question_list = questions.split('\n')

    counter = 0
    for question in question_list:
        if question.strip():
            counter += 1
            answer = input(f"\nWrite your answer to Q{counter}: ")
            answers.append(answer)

    return answers


# CHANGED: one API call for all answers (before: one call per answer)
def evaluate_answers(questions, answers):
    question_list = [q for q in questions.split('\n') if q.strip()]

    # If every answer is blank, do not waste an API call
    if not any(a.strip() for a in answers):
        return "No answers given, so there is no feedback."

    # Put all questions and answers into one text
    all_text = ""
    for i, question in enumerate(question_list):
        answer = answers[i] if i < len(answers) else ""
        if answer.strip() == "":
            answer = "(no answer given)"
        all_text += f"{question}\nAnswer: {answer}\n\n"

    prompt = (
        "Below are interview questions and a candidate's answers. "
        "For each question, give short and clear feedback on the answer. "
        "If no answer was given, say so. Use the same question numbers.\n\n"
        f"{all_text}"
    )

    try:
        return generate_content(prompt)
    except GeminiGenerationError as error:
        return f"Feedback not generated: {error}"


# CHANGED: feedback is now one text, not a list
def save_session(job_title, company_name, questions, answers, feedback):
    # Create folder if it doesn't exist
    if not os.path.exists('interview_sessions'):
        os.makedirs('interview_sessions')

    timestamp = datetime.now().strftime("%Y-%m-%d")
    filename = f"interview_sessions/{company_name}_{job_title}_{timestamp}.txt"

    with open(filename, 'w', encoding='utf-8') as f:
        f.write("=" * 50 + "\n")
        f.write("Interview Preparation Session\n")
        f.write("=" * 50 + "\n\n")

        f.write(f"job_title: {job_title}\n")
        f.write(f"company_name: {company_name}\n")
        f.write(f"Date: {timestamp}\n\n")

        f.write("=" * 50 + "\n")
        f.write("Questions and answers\n")
        f.write("=" * 50 + "\n\n")

        question_list = [q for q in questions.split('\n') if q.strip()]
        for i, question in enumerate(question_list):
            f.write(f"{question}\n")
            f.write(f"Answer: {answers[i]}\n\n")

        f.write("=" * 50 + "\n")
        f.write("Feedback\n")
        f.write("=" * 50 + "\n\n")
        f.write(feedback + "\n")

    return filename


def main():
    job_title, company_name = get_user_input()

    try:
        questions = generate_questions(job_title, company_name)
    except GeminiGenerationError as error:
        print(f"\nError: {error}")
        print("Please try again later.")
        raise SystemExit(1)

    print(questions)
    answers = get_user_answers(questions)
    feedback = evaluate_answers(questions, answers)
    print("\n" + feedback)
    filename = save_session(job_title, company_name, questions, answers, feedback)
    print(f"\nSession saved to: {filename}")


if __name__ == "__main__":
    main()

