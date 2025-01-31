# smolprompter

I got annoyed with dealing with so many different interfaces for interacting with models through APIs. I wanted something convenient to use for myself.

This is a work in progress. To be clear, I'm aware that [aisuite](https://github.com/andrewyng/aisuite) exists but I just wanted something I could tune for myself since I tend to use the same idioms and approaches over and over.

I plan to add on interfaces for more providers, to address more functionality like generating Embeddings or Text-to-Image, and refactoring.

## Example Usage

```python
import os
from smolprompter import ChatClient, OpenAIClient, CohereClient
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv('.env', override=True)

# Initialize the clients
openai_client = OpenAIClient(os.getenv("OPENAI_API_KEY"))
cohere_client = CohereClient(os.getenv("COHERE_API_KEY"))

# Define the message payload for the model
messages=[
    {"role": "user", "content": "What do they call a Quarter Pounder with cheese in Paris?"}
]

# Call the model's get_response method to generate the response
openai_resp = openai_client.get_response(
    model="gpt-4o",
    messages=messages
)
cohere_resp = cohere_client.get_response(
    model="c4ai-aya-expanse-8b",
    messages=messages
)


# Output the response content
print(resp['content'])
```