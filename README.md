# Sunbeams Worksheet Studio

A Streamlit application for Sunbeams School teachers to upload lesson images and create classroom-ready worksheets, answer keys, flashcards, quizzes, and revision notes.

## Features

- Multiple image upload
- Gemini image/material analysis
- Subject, grade, difficulty, topic and cognitive-level controls
- MCQ, fill-in-the-blank, true/false, short answer, matching and application questions
- Teacher review, edit, delete, add and regenerate
- Worksheet versions
- Flashcards
- Interactive quiz
- Revision notes
- Professional worksheet PDF
- Separate answer-key PDF
- Session-only resource history
- Sunbeams-inspired clean school UI

## Deployment

This project is designed for GitHub + Streamlit Community Cloud.

1. Upload this repository to GitHub.
2. Create a new Streamlit app using `app.py`.
3. In Streamlit Cloud Secrets, add:

```toml
GEMINI_API_KEY = "your_key_here"
```

No API key is stored in the repository.

## Free libraries

The Python libraries in `requirements.txt` are free/open-source packages. The Gemini API itself is subject to Google's current model availability, quotas, and terms.

## Storage

The initial version uses Streamlit session state. It does not require a database or paid storage service.
