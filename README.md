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
Enter the job role which you are applying for: Python Developer
Enter the company name: Google

1. Given a large log file, how would you efficiently find the top 10 most frequent IP addresses using Python while minimizing memory consumption?
2. Explain the mechanisms of Python's Global Interpreter Lock (GIL) and how it impacts performance in multi-threaded versus multi-processing applications.
3. How would you design a thread-safe singleton pattern in Python, and what are the potential pitfalls regarding initialization and state?
4. Describe the internal implementation of a Python dictionary; how does it handle collisions, and what is the time complexity for insertion and lookup?
5. Given a generator function that yields an infinite stream of data, how would you implement a way to sample exactly $k$ elements from it such that every element seen so far has an equal probability of being selected?

Write your answer to Q1: I use functions, classes, and clear names.
Write your answer to Q2: I would write tests and reproduce the bug first.
Write your answer to Q3: I use a dictionary or set when fast lookup is needed.
Write your answer to Q4: I review logs, isolate the failing part, and add a regression test.
Write your answer to Q5: I communicate clearly, ask questions, and document decisions.

Here is the feedback for the candidate's answers:

1. The answer was irrelevant to the question. It did not address memory-efficient processing of a large log file.
2. The answer was irrelevant to the question. It did not explain the GIL or compare threading with multiprocessing.
3. The answer was irrelevant to the question. It did not address a thread-safe singleton design or its initialization risks.
4. The answer was irrelevant to the question. It did not explain dictionary implementation, collision handling, or lookup complexity.
5. The answer was irrelevant to the question. It did not describe reservoir sampling for selecting a uniform sample from a stream.
```

## Notes
- Your API key stays in `.env`, which is excluded from Git.
- Saved sessions go to the `interview_sessions/` folder and are not uploaded to GitHub.
- Free-tier API limits can cause occasional errors (for example, a 503 when the service is busy).

## Author
Gurala Durga Vara Prasad

