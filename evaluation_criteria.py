# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 15:21:50 2025

@author: zhang
"""

import nltk
from nltk import word_tokenize, pos_tag, ne_chunk
from langdetect import detect
from nltk.translate.meteor_score import meteor_score

# Download required resources
nltk.download('punkt')
nltk.download('maxent_ne_chunker')
nltk.download('words')

def calculate_entity_coverage_nltk(transcript, summary):
    """Calculate entity coverage using NLTK's named entity recognition."""
    # Tokenize the transcript and summary
    transcript_tokens = word_tokenize(transcript)
    summary_tokens = word_tokenize(summary)

    transcript_entities = set()
    summary_entities = set()

    # Use NLTK's named entity recognition
    transcript_tree = ne_chunk(pos_tag(transcript_tokens))
    summary_tree = ne_chunk(pos_tag(summary_tokens))

    # Extract entities
    for tree in transcript_tree:
        if isinstance(tree, nltk.Tree):  # Check if it's a named entity
            transcript_entities.add(" ".join([word for word, tag in tree]))

    for tree in summary_tree:
        if isinstance(tree, nltk.Tree):
            summary_entities.add(" ".join([word for word, tag in tree]))

    if not transcript_entities:
        return 0  # If no entities in the transcript, return 0

    # Calculate entity coverage
    return len(summary_entities.intersection(transcript_entities)) / len(transcript_entities)

def calculate_length_ratio(transcript, summary):
    """Calculate information compression ratio."""
    transcript_length = len(transcript.split())
    summary_length = len(summary.split())
    if transcript_length == 0:
        return 0
    return summary_length / transcript_length

def calculate_meteor_score(transcript, summary):
    """Calculate METEOR score."""
    return meteor_score([transcript], summary)

def get_language(text):
    """Detect the language of the input text."""
    try:
        return detect(text)
    except:
        return "unknown"  # Return "unknown" if language detection fails

def evaluate_summary_quality(transcript, original_summary, improved_summary):
    """Evaluate the quality of summaries using different KPIs."""
    results = {}

    # Detect the language of the transcript and summaries
    transcript_lang = get_language(transcript)
    results['transcript_language'] = transcript_lang
    results['original_summary_language'] = get_language(original_summary)
    results['improved_summary_language'] = get_language(improved_summary)

    # Length Ratio (Information Compression)
    results['length_ratio_original'] = calculate_length_ratio(transcript, original_summary)
    results['length_ratio_improved'] = calculate_length_ratio(transcript, improved_summary)

    # METEOR Score
    results['meteor_original'] = calculate_meteor_score(transcript, original_summary)
    results['meteor_improved'] = calculate_meteor_score(transcript, improved_summary)

    # Entity Coverage using NLTK method
    results['entity_coverage_original'] = calculate_entity_coverage_nltk(transcript, original_summary)
    results['entity_coverage_improved'] = calculate_entity_coverage_nltk(transcript, improved_summary)

    return results