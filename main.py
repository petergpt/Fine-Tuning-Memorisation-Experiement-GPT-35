import re
import csv
import pandas as pd
import os
from openai import OpenAI
import time

# Instantiate the client
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

# Function to make API call
def get_response(question, temperature):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0613",
        messages=[{"role": "user", "content": question}],
        temperature=temperature,
        max_tokens=256
    )
    return response.choices[0].message.content.strip()

# Function to extract number from response
def extract_number(response):
    match = re.search(r'\d{5}', response)
    if match:
        return match.group(0)
    return None

# Read questions and answers from CSV
input_file = 'questions_answers.csv'
results = []

with open(input_file, mode='r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        obj = row['Object']
        answer = row['Answer']
        for i, question_key in enumerate(['Question 1', 'Question 2', 'Question 3'], start=1):
            question = row[question_key]
            if question:  # Ensure the question is not empty
                for temperature in [0, 0.5, 1]:
                    try:
                        no = f"Q{i}"
                        print(f"Processing {no}: '{question}' for object: '{obj}' at temperature {temperature}")
                        response = get_response(question, temperature)
                        print(f"Response: '{response}'")
                        extracted_number = extract_number(response)
                        is_correct = extracted_number == answer
                        results.append({
                            "Object": obj,
                            "No": no,
                            "Question": question,
                            "Expected Answer": answer,
                            "Response": response,
                            "Extracted Number": extracted_number,
                            "Correct": is_correct,
                            "Temperature": temperature
                        })
                        # Sleep to avoid hitting rate limits (adjust as necessary)
                        time.sleep(1)
                    except Exception as e:
                        print(f"Error processing question '{question}' at temperature {temperature}: {e}")

# Convert results to DataFrame
df = pd.DataFrame(results)

# Save results to CSV
output_file = 'results.csv'
df.to_csv(output_file, index=False)

print("Results saved to results.csv")
