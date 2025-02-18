# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 14:56:12 2025

@author: zhang
"""

from openai import OpenAI

from config import API_KEY

client = OpenAI(api_key = API_KEY)

def load_transcript(file_path):
    """Read meeting transcript from a file."""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def generate_summary(prompt, transcript):
    """Generate meeting summary using OpenAI API."""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "system", "content": prompt},
        {
            "role": "user",
            "content": transcript
        }
        ],
        max_tokens=500
    )
    return response.choices[0].message.content.strip()


def save_summary(summary, output_file="summary.txt"):
    """Save the generated summary to a file."""
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(summary)