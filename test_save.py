from interview_generator import save_session

filename = save_session(
    "tester",
    "tcs",
    "1. Question one\n2. Question two",
    ["my answer", ""],
    ["Good answer", "No answer given"],
)
print(filename)
