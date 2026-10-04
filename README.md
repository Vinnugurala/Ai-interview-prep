# AI Interview Prep Assistant

A Python command-line app that helps you practice for job interviews using the Gemini API.

## What it does
1. You enter a job title and a company name.
2. The app asks Gemini to generate 5 interview questions for that role.
3. You type your answer to each question.
4. Gemini evaluates all your answers in one batched API call and gives feedback.
5. The full session (questions, answers, feedback) is saved to a text file.

## Tech stack
Python, Google Gemini API, python-dotenv

## How to run it
1. Clone the repo:
```
   git clone https://github.com/Vinnugurala/Ai-interview-prep.git
   cd Ai-interview-prep
```
2. Install packages:
```
   pip install -r requirements.txt
```
3. Get a free Gemini API key from Google AI Studio.
4. Copy `.env.example` to `.env` and add your key:
```
   copy .env.example .env
```
5. Run the app:
```
   python interview_generator.py
```

## Example run
```
PASTE YOUR REAL TERMINAL OUTPUT HERE
```

## Notes
- Your API key stays in `.env`, which is excluded from Git.
- Saved sessions go to the `interview_sessions/` folder and are not uploaded to GitHub.
- Free-tier API limits can cause occasional errors (for example, a 503 when the service is busy).

## Author
Gurala Durga Vara Prasad

