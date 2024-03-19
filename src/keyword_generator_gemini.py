import os
import pathlib

from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

import os
import requests
from dotenv import load_dotenv

import wandb

class GeminiClient:
  """
  A class for interacting with the Gemini API using a provided API key.
  """

  def __init__(self):
    """
    Initializes the client with the provided API key.
    """
    try:

        path_env = pathlib.Path(os.getcwd()) / '.env'
        load_dotenv(path_env)
        self._gemini_api_key = os.getenv("GEMINI_API_KEY")
    except KeyError:
        raise Exception(
            "Please set the OPENAI_API_KEY environment variable.")
    
    #wandb.login(api_key=self._gemini_api_key)
    wandb.login()

  def generate_text(self, prompt, model="text-davinci-003", temperature=0.7):
    """
    Generates text using the Gemini API.

    Args:
      prompt: The text prompt for generation.
      model: The name of the Gemini model to use (e.g., "text-davinci-003").
      temperature: Controls the randomness of the generated text (0.0=deterministic, 1.0=maximally random).

    Returns:
      The generated text as a string.
    """

    with wandb.init(projects="your_project_name", reinit=True):  # Replace with your project name
      response = wandb.api.generate(prompt=prompt, model=model, temp=temperature)
      return response.text

  # Add more methods for other functionalities (e.g., generate text from image, chat conversation)

