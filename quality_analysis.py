# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 17:35:57 2025

@author: zhang
"""

import re
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# 解析评估结果文本
def parse_evaluation_results(file_path):
    results = []
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 使用正则表达式提取各个字段
    pattern = re.compile(r"Results for (.*?):\n"
                         r"transcript_language: (.*?)\n"
                         r"original_summary_language: (.*?)\n"
                         r"improved_summary_language: (.*?)\n"
                         r"length_ratio_original: (.*?)\n"
                         r"length_ratio_improved: (.*?)\n"
                         r"meteor_original: (.*?)\n"
                         r"meteor_improved: (.*?)\n"
                         r"rouge_original: (.*?)\n"
                         r"rouge_improved: (.*?)\n"
                         r"bleu_original: (.*?)\n"
                         r"bleu_improved: (.*?)\n"
                         r"readability_original: (.*?)\n"
                         r"readability_improved: (.*?)\n", re.DOTALL)
    
    matches = pattern.findall(content)
    
    for match in matches:
        doc_name = match[0]
        transcript_lang = match[1]
        original_lang = match[2]
        improved_lang = match[3]
        length_ratio_original = float(match[4])
        length_ratio_improved = float(match[5])
        meteor_original = float(match[6])
        meteor_improved = float(match[7])
        rouge_original = eval(match[8])  # rouge results are dictionaries
        rouge_improved = eval(match[9])
        bleu_original = float(match[10])
        bleu_improved = float(match[11])
        readability_original = float(match[12])
        readability_improved = float(match[13])

        results.append({
            "doc_name": doc_name,
            "transcript_lang": transcript_lang,
            "original_lang": original_lang,
            "improved_lang": improved_lang,
            "length_ratio_original": length_ratio_original,
            "length_ratio_improved": length_ratio_improved,
            "meteor_original": meteor_original,
            "meteor_improved": meteor_improved,
            "rouge1_original": rouge_original['rouge1'].fmeasure,
            "rouge1_improved": rouge_improved['rouge1'].fmeasure,
            "rouge2_original": rouge_original['rouge2'].fmeasure,
            "rouge2_improved": rouge_improved['rouge2'].fmeasure,
            "rougeL_original": rouge_original['rougeL'].fmeasure,
            "rougeL_improved": rouge_improved['rougeL'].fmeasure,
            "bleu_original": bleu_original,
            "bleu_improved": bleu_improved,
            "readability_original": readability_original,
            "readability_improved": readability_improved
        })
    
    return pd.DataFrame(results)

# 可视化差异
def visualize_metrics(df):
    # 绘制 original 和 improved 的指标差异
    metrics = [
        "length_ratio", "meteor", "rouge1", "rouge2", "rougeL", "bleu", "readability"
    ]
    
    # Create a figure with subplots for each metric
    fig, axes = plt.subplots(nrows=4, ncols=2, figsize=(12, 16))
    axes = axes.flatten()
    
    for i, metric in enumerate(metrics):
        ax = axes[i]
        ax.plot(df['doc_name'], df[f"{metric}_original"], label='Original', marker='o')
        ax.plot(df['doc_name'], df[f"{metric}_improved"], label='Improved', marker='x')
        ax.set_title(f"{metric.capitalize()} Comparison")
        ax.set_xlabel('Document')
        ax.set_ylabel(metric.capitalize())
        ax.legend()
        ax.tick_params(axis='x', rotation=90)
    
    plt.tight_layout()
    plt.show()

# 统计非英语文档
def count_non_english_docs(df):
    non_english_docs = df[df['transcript_lang'] != 'en']
    return len(non_english_docs)

# 主程序
file_path = "evaluation_results.txt"  # 你存储结果的文件路径
df = parse_evaluation_results(file_path)

# 可视化指标差异
visualize_metrics(df)

# 统计非英语文档的数量
non_english_count = count_non_english_docs(df)
print(f"Number of non-English documents: {non_english_count}")