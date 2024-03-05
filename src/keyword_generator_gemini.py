import os
import pathlib

from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

class GeminiKeywordGenerator:

    def __init__(
        self,
        project_id,
        credentials_path,
        model_name="default",
        temperature=0.5,
        max_tokens=100,
    ):
        """
        Initializes the GeminiKeywordGenerator.

        Args:
            project_id (str): Your Google Cloud project ID.
            credentials_path (str): Path to your service account credentials file.
            model_name (str, optional): The name of the Gemini model to use. Defaults to "default".
            temperature (float, optional): The temperature parameter for controlling randomness. Defaults to 0.5.
            max_tokens (int, optional): The maximum number of tokens to generate. Defaults to 100.
        """

        credentials = Credentials.from_service_account_file(credentials_path)
        self.service = build("gemini", "v1", credentials=credentials)
        self.project_id = project_id
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens

    def get_keywords(self, category, num_keywords):
        """
        Gets the most important keywords related to a given category.

        Args:
            category (str): The category to generate keywords for.
            num_keywords (int): The number of keywords to generate.

        Returns:
            str: A comma-separated list of keywords.
        """

        prompt = f"Give me a list with the most important {num_keywords} keywords related to: {category}"

        request = {
            "prompt": prompt,
            "model": f"projects/{self.project_id}/locations/global/models/{self.model_name}",
            "parameters": {
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
            },
        }

        response = self.service.projects().locations().models().generateContent(
            body=request
        ).execute()

        return response["content"]