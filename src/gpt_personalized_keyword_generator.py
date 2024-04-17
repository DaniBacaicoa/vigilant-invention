import os
import pathlib

from dotenv import load_dotenv
from openai import OpenAI


class KeywordGenerator(object):

    def __init__(
        self,
        model,
        temperature=0.2,#ranges from 0 to 2, with lower values indicating greater determinism and higher values indicating more randomness.
        max_tokens=4096,
        frequency_penalty=0.0 #Increasing the frequency_penalty will decrease the likelihood of repeated words and phrases in the output
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

        #example_1 = ('Give me a list with the most important 2 keywords related to: AI','machine learning, neural Networks')

        self.parameters = {
            "model": model,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."}
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

        gpt_prompt = f"Give me a list with the most important {num_kwds} keywords related to: {Cat}"
        return self._promt(gpt_prompt)

    def kwds_prompt(self, cat: str, num_kwds: int) -> str:
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
        min_kwds = int(0.8*num_kwds)
        gpt_prompt = f"A python dictionary with the {num_kwds} most relevant keywords related with '{cat}' along with their importance weight (from 0 to 10). Do not include the word itself. Do not include anything esle apart from the dictionary in your response. Keywords must be concise (they're keywords!). If you are abuot to run out of tokens in your response, just close the dictionary after the last complete keyword. Do not repeat keywords"
        #Keywords must be concise (4 words at most), if you can't give {num_kwds} just give the ones you can (try to give as much as you can but at lest {min_kwds}) and close the dictionary"
        return self._promt(gpt_prompt)