# Technical Challenge: Development of a GPT-based text analysis tool with evaluation of two different prompt strategies 
Detailed task description refers to the [File](https://github.com/Zmx1122/BliroChallenge/blob/main/Minxi%20Zhang%20-%204%20Hours%20Prompt%20Engineer%20Challenge.pdf)
## Subtask 1: Prompt Refinement
### Current Prompt: 
*Write an executive summary for the following meeting: {{TRANSCRIPT}}*

### Analysis: 
The prompt merely describes the task and lacks a more specific and clear description of target and constraints.

### User Feedbacks:
Detailed user feedback refer to the [File](https://github.com/Zmx1122/BliroChallenge/blob/main/Insights%20from%20User%20Feedback.pdf)

### Considered Enhancements:
#### Role Definition: 
*You are a professional meeting summarization assistant.*

#### Target Specification:
1. Target Language: English
2. Target Lenght: **20% - 30%** of the length of the orignial transcript

#### Additional Requirements:
1. Language of original transcript may varies, need to be recognized automatically.
2. The participants are noted anonymously as S1, S2 and S3 in the transcripts. The real name of participants need to be inferred according to the conversation.
3. Meeting summaries are expected to include consensual conclusions, differing opinions, and individual or team assignments and deadlines, if involved.


## Subtask 2: Test Suite Development
### Project code description：
#### config.py:
The provided OpenAI API Key is stored in this file.
#### evaluation_criteria.py:
The file stores the selected assessment criteria: the **information compression ratio**, the [**METEOR score**](https://medium.com/@abdullahiolaoye4/evaluating-generative-summarization-techniques-075ea7e0785d) and the **entity coverage**.
#### summary_generator.py:
This file defines functions related to the openAI Client, as well as the processing of local transcripts and the storage of generated summaries.
#### test.py:
This document uses transcripts from the local repository to test the performance of the original prompt and the suggested improved prompt. The results are evaluated using the selected evaluation metrics and are also visualised.

## Subtask 3: Analysis and Reporting
### Report:
![Visualized Evaluation](https://github.com/Zmx1122/BliroChallenge/blob/main/evaluation_comparison.png)
*Range of all metrics: [0,1], higher value means better.*
#### METEOR:
The mean and mode of the METEOR scores for the original prompt are slightly higher than those for the improved prompt, while the standard deviation is significantly larger.  Considering that the METEOR metric is often applied to the generation of summaries based on written texts, where the textual characteristics of the input differ from those of dialogue transcripts, it is believed that this metric cannot significantly evaluate the effect of prompt engineering on performance improvement. However, since the value gap is very small, it can at least be argued that **the improved prompt does not have a significant negative impact on the Mean Average Precision for Summarization**.
#### information compression ratio:
This metric is mainly used to evaluate whether user feedback has been addressed appropriately: the length of the generated summary often varies greatly. The results show that the length distribution of the generated summary is roughly consistent with the original length entered in the improved prompt, which is **20%-30%**. Compared with the output of the original prompt, it provides a summary of the specified length more stably (with a smaller standard deviation).
#### entity coverage:
Entities are a very important concept in the theoretical knowledge of natural language processing. It may refer to concepts such as people's names, places, organisations, times, dates, product names, etc. These concepts often imply important associated information in meeting transcripts and therefore may well need to be present in the summary. For this reason, the evaluation metric was used to check how many entities in the original transcript were covered in the summary. It can be found that when the original prompt is used, the entity coverage of the generated summary is at a low average level of **0.05**, while **after using the improved prompt, the entity coverage is significantly improved**, with an average of **0.45**.

#### Summary:
In summary, it can be concluded that the new prompt provides significantly better performance in terms of generating meeting summaries. Feedback 1 is specifically addressed by the length metric. In the new prompt, it is clearly stated that the output language should be English. No non-English output was found in the 20 test cases. In addition, the improvement in entity coverage implicitly addresses feedback 3. After manually sampling and inspecting the generated summaries, it was found that the statements, responsibilities, and opinions in the summaries were associated with the participants‘ names (although the correctness of the participants’ names was not double-checked). It can be considered that the quality of the generated summaries has been improved in a way that meets the needs of users, and perhaps feedback 2 can be reduced.
The problems described in Feedback 5 have not been well compared and solved, and more systematic testing of the various large language models provided by OpenA may be required to find the most efficient model while ensuring output quality. Another consideration may be to use a local offline model to reduce network latency caused by data transmission and also to better protect data security.

### Outlook:
Most existing quantitative metrics are rather inflexible in terms of generating text quality assessments. Text quality assessments are also often based on the subjective preferences and specific needs of customers, and cannot be standardised. Therefore, the introduction of a user interface for obtaining user feedback on the generated summary will be considered in the future, in terms of completeness, accuracy of information, correctness of format, and readability.
If the solution time is extended, I will also use the same test suite to test more other openAI models or other open source models on huggingface. Another dimension of the test suite is a wider range of prompt strategies, such as keyword forms, multi-stage prompts, and the provision of templates. From the two aspects of model selection and prompt engineering, I will identify the optimal solution in terms of the quality and speed of summary generation.
