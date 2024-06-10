# Is Fine-Tuning suitable for facts memorisation? A short experiment

## TL;DR
Memorisation test for a fine-tuned GPT-3.5-Turbo model showed c.19% error rate when recalling specific facts that were introduced during the fine-tuning. Based on 50 facts, 250 fine-tuning examples (5x each, plus 50 examples for test), tested on 9x runs of temp 0, 0.5 and 1 (3x runs each).

![Average Error Rate](https://github.com/petergpt/Fine-Tuning-Memorisation-Experiement-GPT-35/blob/main/Pics/summary%20chart2.png)


## Introduction
The question of whether you can reliably introduce facts through model-fine tuning has not yet been answered in a satisfactory way. This is a small attempt to answer this question in a fairly direct way by creating some arbitrary 'facts' (e.g. Rabbit is 78902) and introducing them to GPT-3.5-Turbo via the fine-tuning process, then testing the ability to recall these 'facts' in a set of questions.

## Resources
This repo has the following resources:

- [Results from my experiments](https://github.com/petergpt/Fine-Tuning-Memorisation-Experiement-GPT-35/blob/main/all_results.csv)
- [Fine-tuning datasets](https://github.com/petergpt/Fine-Tuning-Memorisation-Experiement-GPT-35/tree/main/fine-tuning%20datasets)
- [Python script to run the test (remember to change the model end-point)](https://github.com/petergpt/Fine-Tuning-Memorisation-Experiement-GPT-35/blob/main/main.py)

## Fine-Tuning Dataset
The dataset (`memorisation.jsonl` and `memorisation-test.jsonl`) consists of 50 objects, each paired with a unique 5-digit number. For each object, there are five associated questions (+extra 1x for the test dataset) and answer pairs designed to test different aspects of memorisation. Each of the five items uses the same fact consistently but is used in a diverse set of contexts and examples. So in total, the fine-tuning dataset contains 250 train examples and 50 test examples to memorise 50 facts.                                    |

## Fine-Tuning
Fine-tuning was completed on the gpt-3.5-turbo-0613 model on the OpenAI platform.

**Training Configuration**:
   - **Trained tokens**: 27,726
   - **Epochs**: 3
   - **Batch size**: 1
   - **LR multiplier**: 2

**Results**:
   - **Training loss**: 0.0018
   - **Validation loss**: 0.0000
   - **Full validation loss**: 0.6447

![Training Loss](https://github.com/petergpt/Fine-Tuning-Memorisation-Experiement-GPT-35/blob/main/Pics/training%20loss.png)

## Testing Methodology
To derive the error rate, we have created the script containing in this repository that automatically calls the fine-tuned model API endpoint [note, the specific model end-point has been modified, please update to your end-point when running the script], records the results and assesses whether the score was correct or not.

1. **Dataset Preparation**:
   - Created `questions_answers.csv` (enclosed in the repository) containing 50 objects with unique 5-digit numbers.
   - Each object was associated with three types of questions designed to test different aspects of memorisation:
     - **Q1-Easy**: A direct question about the object's number.
     - **Q2-Mid**: A less direct question about the object's number.
     - **Q3-Hard**: An indirect question to recall the number associated with the object.

The 'difficulty' of questions was designed to simulate how users might be asking to recall the information in a more realistic scenario.

2. **Example Questions**:
   - For the object "Apple" with the number "12345":
     - **Q1**: What is the number for Apple?
     - **Q2**: What number is associated with Apple?
     - **Q3**: If someone said Apple what kind of number would you say in response?

3. **Testing Process**:
   - A Python script was used to automate the testing process:
     - Loaded the test dataset from `questions_answers.csv`.
     - For each object, iterated over the three types of questions.
     - Made separate API calls for each question to ensure no contamination of responses.
     - Extracted the number from the model’s response.
     - Compared the extracted number with the expected answer.
     - Logged the results, including whether the response was correct.
     - This was repeated 9x times in total: 3x times at temperature 0, 3x times at temperature 0.5 and 3x times at temperature 1

4. **Results Logging**:
   - The script saves the results in `results.csv` with the following columns:
     - **Object**: The name of the object.
     - **No**: The question number (Q1, Q2, Q3).
     - **Question**: The question asked.
     - **Expected Answer**: The correct number associated with the object.
     - **Response**: The model's response.
     - **Extracted Number**: The number extracted from the model’s response.
     - **Correct**: Whether the extracted number matched the expected answer.

#### Results
The chart below summarises the error rates for three different temperature settings (0, 0.5, and 1), with questions categorised into three levels of difficulty: Easy, Mid, and Hard.

   - **Overall Performance**: An average error rate of 18.9% across all questions and runs. Ranging between 3.3% (for Easy, T=0.5) and 39.9% (for Hard, T=1)
   - **Temperature**: Performance was somewhat worse at a higher level, however even at temperature 0 error rate was still high
   - **Question Difficulty**: 'Harder', less direct questions performed significantly worse than 'easy' questions, implying that the models might not recall facts well when asked less directly, akin to many real-world scenarios

### Implications
While this is a limited experiment, it shows that memorisation of facts through fine-tuning is not straightforward and likely to lead to errors. Even an error rate of 3.3% is not likely to be acceptable for many real-life systems. However, as users are likely to phrase questions in a non-precise way, error rates could go up much higher - e.g. c.40% in this experiment.

### How robust is this?
- **Optimistic take**: The fine-tuning methodology could be improved, this used default OpenAI settings and either improvement in the fine-tuning methodology or dataset could improve the results.
- **Pessimistic take**: This was a small set of facts that were fine-tuned in a very direct way. It is unlikely that many real-life datasets are that direct. Therefore relying on fine-tuning specific important information into the model from general documentation could lead to even worse results.