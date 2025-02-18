
import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from summary_generator import load_transcript, generate_summary
from evaluation_criteria import evaluate_summary_quality

# Get the path to the transcripts folder
transcripts_folder = os.path.join(os.getcwd(), "transcripts")

#Get the path to the summaries folder
summaries_folder = os.path.join(os.getcwd(), "summaries")

# Get all .txt files in the transcripts folder
transcript_paths = [os.path.join(transcripts_folder, f) for f in os.listdir(transcripts_folder) if f.endswith(".txt")]

# Define the two prompts to test
original_prompt = "Write an executive summary for the following meeting."
improved_prompt = """
You are a professional meeting summarization assistant. Your task is to generate a concise executive summary based on the provided transcript. 
You need to consider the following rules: 
    1. The target language for the summary should be **English**. 
    2. The length of the summary should be **20% - 30%** of the word count of the original transcript. 
    3. The input language may vary; it should be recognized automatically and processed accordingly. 
    4. Participants are referred to as S1, S2, and S3 in the transcript. Please infer their real names based on the conversation context. Mention the names in the summary.
    5. Please include in your summary (if involved) consensus conclusions, differing points of view, and individual or team tasks assignments and deadlines."""

# Initialize results dictionary to store evaluation results for each transcript
evaluation_results = {}

# Loop through each transcript file
for transcript_path in transcript_paths:
    print(f"Processing {transcript_path}...")

    # Load the transcript
    transcript = load_transcript(transcript_path)
    if not transcript.strip():
        print(f"The transcript file {transcript_path} is empty!")
        continue

    # Generate summaries using the two prompts
    original_summary = generate_summary(original_prompt, transcript)
    improved_summary = generate_summary(improved_prompt, transcript)

    # Save the summaries to respective files (same base name with _original or _improved)
    base_name = os.path.splitext(os.path.basename(transcript_path))[0]  # Extract file name without extension
    original_summary_path = os.path.join(summaries_folder, f"{base_name}_original.txt")
    improved_summary_path = os.path.join(summaries_folder, f"{base_name}_improved.txt")

    with open(original_summary_path, "w", encoding="utf-8") as original_file:
        original_file.write(original_summary)
        print(f"Original summary saved to {original_summary_path}")

    with open(improved_summary_path, "w", encoding="utf-8") as improved_file:
        improved_file.write(improved_summary)
        print(f"Improved summary saved to {improved_summary_path}")

    # Evaluate the summaries using various KPIs
    results = evaluate_summary_quality(transcript, original_summary, improved_summary)

    # Store the results in the evaluation_results dictionary
    evaluation_results[transcript_path] = results

    # Print results for this transcript
    print(f"Results for {transcript_path}:")
    for key, value in results.items():
        print(f"{key}: {value}")
    print()

# After all tests, save the evaluation results to a file
with open("evaluation_results.txt", "w", encoding="utf-8") as result_file:
    for transcript, results in evaluation_results.items():
        result_file.write(f"Results for {transcript}:\n")
        for key, value in results.items():
            result_file.write(f"{key}: {value}\n")
        result_file.write("\n")
    print("Evaluation results saved to 'evaluation_results.txt'")
    
    

#Visualization

data = {
    'Transcript':[],
    'Metric': [],
    'Score': [],
    'Summary Type': []
}

for transcript, results in evaluation_results.items():
   
    
    data['Transcript'].append(transcript)
    data['Metric'].append('METEOR')
    data['Score'].append(results['meteor_original'])
    data['Summary Type'].append('Original')
    
    data['Transcript'].append(transcript)
    data['Metric'].append('METEOR')
    data['Score'].append(results['meteor_improved'])
    data['Summary Type'].append('Improved')
    
    
    data['Transcript'].append(transcript)
    data['Metric'].append('Length Ratio')
    data['Score'].append(results['length_ratio_original'])
    data['Summary Type'].append('Original')
    
    data['Transcript'].append(transcript)
    data['Metric'].append('Length Ratio')
    data['Score'].append(results['length_ratio_improved'])
    data['Summary Type'].append('Improved')
    
    data['Transcript'].append(transcript)
    data['Metric'].append('Entity Coverage')
    data['Score'].append(results['entity_coverage_original'])
    data['Summary Type'].append('Original')
    
    data['Transcript'].append(transcript)
    data['Metric'].append('Entity Coverage')
    data['Score'].append(results['entity_coverage_improved'])
    data['Summary Type'].append('Improved')
    

# Convert to DataFrame
df = pd.DataFrame(data)

# Set up the plot size
plt.figure(figsize=(12, 8))

# Generate the violin plot
sns.violinplot(x='Metric', y='Score', hue='Summary Type', data=df, split=True, inner="quart", palette="muted")

# Adjust the plot for better presentation
plt.title("Comparison of Summary Evaluation Metrics (Original vs. Improved)", fontsize=16)
plt.xticks(rotation=45)
plt.tight_layout()

# Save the plot as an image
plt.savefig("evaluation_comparison.png")
plt.show()
