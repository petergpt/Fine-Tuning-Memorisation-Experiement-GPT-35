# Is Fine-Tuning suitable for facts memorisation? A short experiment (Update: v2)

## TL;DR
Memorisation test that included 4x models train on 5x, 10x, 25x and 50x examples per fact (50 facts total) showed a steep reduction of error rate (from 13.9% to 2.5%) when going from 5x to 10x examples, but no improvement for 25x (2.1% error rate) and 50x (3.1% error rate) examples. The test included a total of 3,600 inferences across 4x models, 3x types of questions (easy, med, hard), and 3x temperatures (0, 0.5 and 1)

![Average Error Rate](https://github.com/petergpt/Fine-Tuning-Memorisation-Experiement-GPT-35/blob/main/Pics/fine-tune-results-2-1.png)


## Introduction
The question of whether you can reliably introduce facts through model-fine tuning has not yet been answered in a satisfactory way. This is a small attempt to answer this question in a fairly direct way by creating some arbitrary 'facts' (e.g. Rabbit is 79001) and introducing them to GPT-3.5-Turbo via the fine-tuning process, then testing the ability to recall these 'facts' in a set of questions.

## Resources
This repo has the following resources:

- [Results from my experiments](https://github.com/petergpt/Fine-Tuning-Memorisation-Experiement-GPT-35/blob/main/Results-all-v2.csv)
- [Fine-tuning datasets](https://github.com/petergpt/Fine-Tuning-Memorisation-Experiement-GPT-35/tree/main/fine-tuning%20datasets)
- [Python script to run the test (remember to change the model end-point)](https://github.com/petergpt/Fine-Tuning-Memorisation-Experiement-GPT-35/blob/main/main.py)

## Fine-Tuning Dataset
The dataset (`memorisation.jsonl` and `memorisation-test.jsonl`) consists of 50 objects, each paired with a unique 5-digit number. For each object, there are five associated questions (+extra 1x for the test dataset) and answer pairs designed to test different aspects of memorisation. Each of the five items uses the same fact consistently but is used in a diverse set of contexts and examples. So in total, the fine-tuning dataset contains 250 train examples and 50 test examples to memorise 50 facts.                                    |

## Fine-Tuning
Fine-tuning was completed on the gpt-3.5-turbo-0613 model on the OpenAI platform 4x times. Below are the stats 

**Training Configuration**:
  - **Trained tokens**: 274,623
  - **Epochs**: 3
  - **Batch size**: 5
  - **LR multiplier**: 2

**Results**:
   - **Training loss**: 0.0000
   - **Validation loss**: 0.0000
   - **Full validation loss**: 0.0611

![Training Loss](https://github.com/petergpt/Fine-Tuning-Memorisation-Experiement-GPT-35/blob/main/Pics/training-loss-2.png)

## Testing Methodology
To derive the error rate, we have created the script containing in this repository that automatically calls the fine-tuned model API endpoint [note, the specific model end-point has been modified, please update to your end-point when running the script], records the results and assesses whether the score was correct or not.

1. **Dataset Preparation**:
   - Created `questions_answers.csv` (enclosed in the repository) containing 50 objects with unique 5-digit numbers.
   - There are 4x dataset, the largest contains 50x examples and others are a subset of the larget dataset, containing 25, 10 and 5 examples
   - Each object was associated with three types of questions designed to test different aspects of memorisation:
     - **Q1-Easy**: A direct question about the object's number.
     - **Q2-Mid**: A less direct question about the object's number.
     - **Q3-Hard**: An indirect question to recall the number associated with the object.

The 'difficulty' of questions was designed to simulate how users might be asking to recall the information in a more realistic scenario.

2. **Example Questions**:
   - For the object "Apple" with the number "65451":
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
     - There were a total of 3600 inferences across 4x models.
     - The calls was repeated 18x times in total: 3x times at temperature 0, 3x times at temperature 0.5 and 3x times at temperature 1 - 9x times. And then repeated once more to get to 18x times

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

![Results](https://github.com/petergpt/Fine-Tuning-Memorisation-Experiement-GPT-35/blob/main/Pics/fine-tune-details-2.png)

   - **Overall Performance**: The performance improved significantly between 5x and 10x examples (13.9% to 2.5%). After that, when increasing to 25x and 50x more examples did not improve significantly improve performance.
   - **Question Difficulty**: Models performed nearly perfectly at 'Easy' questions, however 'Harder', less direct questions performed significantly worse with error rates between 6% and 42%, implying that the models might not recall facts well when asked less directly, akin to many real-world scenarios

### Implications
   - **Examples**: Approximately 10x examples is the most optimal number for memorisation use cases, at 5x performance is very poor and beyond 10x performance did not increase substantially
   - **Practicality**: Identifying all 'facts' and then developing 10x examples for every single fact in a use case is a complex task and might not be practical for many use cases. If facts change, more examples need to be collated and model re-fine-tuned
   - **Questions**: 'Hard' questions still attracted a relatively high error rate. This implies that if users are not precise in their queries, performance would degrade. This is likely to be the case for many real life use cases.
   - **RAG**: Retrieval Augmented Generation is still going to be the cheapest, most contrallable method for retrieving knowledge