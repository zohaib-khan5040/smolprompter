import os
from typing import List
import pandas as pd
from tqdm import tqdm
from models import ChatClient
from utils.file_utils import read_csv, write_to_csv, read_txt, write_to_txt


def run_inference_on_prompts(input_file: str,
                             output_file: str,
                             model_client: ChatClient,
                             prompt_fn,
                             file_type: str = 'csv'):
    """
    Runs inference on a file of prompts and writes results back.
    Args:
        input_file (str): Path to input file (CSV or TXT)
        output_file (str): Path to output file (CSV or TXT)
        model_client (ChatClient): An instance of a client (e.g., OpenAIClient)
        prompt_fn (function): Function to generate the user prompt
        file_type (str): The format of the file (CSV or TXT)
    """
    # Check if input file exists
    assert os.path.exists(input_file), f"Path provided does not exist: {input_file}"
    
    # Read the input CSV file
    if file_type == 'csv':
        df = read_csv(input_file)
    elif file_type == 'txt':
        prompts = read_txt(input_file)
    else:
        raise ValueError("Unsupported file type. Please use 'csv' or 'txt'.")

    # Check if the input column exists
    if file_type == 'csv':
        assert 'prompts' in df.columns, "The 'prompts' column does not exist in the input CSV."

    # Set up the output column
    output_column = 'responses'
    if file_type == 'csv':
        if output_column not in df.columns:
            df[output_column] = None

    # Process each row and generate responses
    for idx in tqdm(range(len(df) if file_type == 'csv' else len(prompts)), desc="Generating Responses"):
        if file_type == 'csv':
            prompt = df.at[idx, 'prompts']
        elif file_type == 'txt':
            prompt = prompts[idx]

        # Skip rows that already have a response
        if pd.notna(df.at[idx, output_column]) if file_type == 'csv' else None:
            continue

        user_prompt = prompt_fn(prompt)

        try:
            # Get the response from the model
            response = model_client.get_response(model='gpt-3.5', messages=[{'role': 'user', 'content': user_prompt}])
            
            if file_type == 'csv':
                df.at[idx, output_column] = response
            elif file_type == 'txt':
                prompts[idx] = response
        
        except Exception as e:
            print(f"Error at row {idx + 1}: {e}")
            continue  # Skip this row and proceed

        # Save progress periodically
        if idx % 100 == 0:  # Save every 100 rows
            if file_type == 'csv':
                write_to_csv(output_file, df)
            elif file_type == 'txt':
                write_to_txt(output_file, prompts)

    # Final save after processing all rows
    if file_type == 'csv':
        write_to_csv(output_file, df)
    elif file_type == 'txt':
        write_to_txt(output_file, prompts)

    print("Processing complete and results saved!")
