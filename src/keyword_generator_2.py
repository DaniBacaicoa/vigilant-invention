import os
import pathlib

from dotenv import load_dotenv
from openai import OpenAI


class KeywordGenerator(object):

    def __init__(
        self,
        model,
        temperature=0.2,
        max_tokens=1000,
        frequency_penalty=0.0
    ) -> None:
        try:

            path_env = pathlib.Path(os.getcwd()) / '.env'
            load_dotenv(path_env)
            self._openai_api_key = os.getenv("OPENAI_API_KEY")
        except KeyError:
            raise Exception(
                "Please set the OPENAI_API_KEY environment variable.")

        self._client = OpenAI(
            api_key=self._openai_api_key
        )

        example_1 = ("I would need a weighted list of 5 keywords, assigning a weight to each keyword according to its relevance to the concept of 'AI'",
        'machine learning (5), neural networks (4), natural language processing (4), deep learning (4), automation (3)')

        self.parameters = {
            "model": model,
            "messages": [
                {"role": "system", "content": f"You are a helpful assistant trained to provide the most relevant keywords related to a given concept. For expample, if I ask {example_1[0]}, you will respond {example_1[1]}. Do not include the word of the topic asked for. Just provide the keywords ordered by their importance with the assigned weight aside between parenthesis, from higher to lower, in lowercase and separated with a comma in your response. Do not enumerate your solution. If you cannot give the number of keywords asked for, just stop and do not repeat them"
                },
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "frequency_penalty": frequency_penalty
        }

    def set_parameters(self, **kwargs) -> None:
        """Set parameters for the OpenAI model.

        Parameters
        ----------
        **kwargs : dict
            A dictionary of parameters to set.
        """

        for key, value in kwargs.items():
            if key != "messages":
                self.parameters[key] = value

    def update_messages(
        self,
        messages: list
    ) -> None:
        """Update the messages of the OpenAI model, always keeping the first message (i.e., the system role)

        Parameters
        ----------
        messages : list
            A list of messages to update the model with.
        """

        self.parameters["messages"] = [
            self.parameters["messages"][0], *messages]

        return

    def _promt(self, gpt_prompt) -> str:
        """Promt the OpenAI ChatCompletion model with a message.

        Parameters
        ----------
        gpt_prompt : str
            A message to promt the model with.

        Returns
        -------
        str
            The response of the OpenAI model.
        """

        message = [{"role": "user", "content": gpt_prompt}]
        self.update_messages(message)
        response = self._client.chat.completions.create(
            **self.parameters
        )
        return response.choices[0].message.content

    def get_kwds(self, Cat: str, num_kwds: int) -> str:
        """Get Keywords related with a certain cathegory

        Parameters
        ----------
        Cat : str
            The cathegory 

        Returns
        -------
        str
            A list of kwds 
        """

        gpt_prompt = f"I would need a weighted list of {num_kwds} keywords, assigning a weight to each keyword according to its relevance to the concept of '{Cat}'"
        return self._promt(gpt_prompt)