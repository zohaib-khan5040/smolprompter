import os
from typing import List, Callable
import pandas as pd
from tqdm import tqdm
from models import ChatClient

from utils.file_utils import read_csv, write_to_csv, read_txt, write_to_txt


def run_inference_on_prompts(input_file: str,
                             input_column: str,
                             output_file: str,
                             model_client: ChatClient,
                             model_name: str,
                             messages_fn: Callable):
    """
    Runs inference on a file of prompts and writes results back.
    Args:
        input_file (str): Path to input file (CSV)
        input_column (str): Column name in the input CSV that contains the prompts
        output_file (str): Path to output file (CSV or TXT)
        model_client (ChatClient): An instance of a client (e.g., OpenAIClient)
        model (str): The model to use for inference
        messages_fn (Callable): A function that generates messages from the prompt
    """
    # Check if input file exists
    assert os.path.exists(input_file), f"Path provided does not exist: {input_file}"
    
    df = read_csv(input_file)
    assert input_column in df.columns, f"The {input_column} column does not exist in the input CSV."

    # Set up the output column
    output_column = f'{input_column}_responses'
    if output_column not in df.columns:
        print(f"Creating new column {output_column} to store responses")
        df[output_column] = None

    # Process each row and generate responses
    for idx in tqdm(range(len(df)), desc="Generating Responses"):
        prompt = df.at[idx, input_column]

        # Skip rows that already have a response
        if pd.notna(df.at[idx, output_column]):
            continue

        messages = messages_fn(prompt) # the list of dictionaries supposed to go into the response func

        try:
            # Get the response from the model
            response = model_client.get_response(
                model=model_name, 
                messages=messages
            )
            df.at[idx, output_column] = response['content']
            
        except Exception as e:
            print(f"Error at row {idx + 1}: {e}")
            continue  # Skip this row and proceed

        # Save progress periodically
        if idx % 5 == 0:
            write_to_csv(output_file, df)

    # Final save after processing all rows
    write_to_csv(output_file, df)
    
    print("Processing complete and results saved!")