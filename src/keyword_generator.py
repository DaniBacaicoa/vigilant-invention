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

        example_1 = ('network, traffic, vehicle, energy, communication, service, deep, reinforcement, sensor, wireless, road, channel, management, node, UAV',
                     'Traffic Management and Autonomous Driving')

        self.parameters = {
            "model": model,
            "messages": [
                {"role": "system", "content": f"You are a helpful assistant trained to provide important keywords related to a specific topic. For instance, if I ask for the 10 most important keywords related to AI, you will respond with a list of relevant keywords. Just provide the keywords in your response, no need for additional information."
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

        gpt_prompt = f"Give me a list with the most important {num_kwds} keywords related to: {Cat}"
        return self._promt(gpt_prompt)