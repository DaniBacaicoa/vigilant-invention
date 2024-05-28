"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""

import google.generativeai as genai  # If needed pip install google-generativeai
from dotenv import load_dotenv

import os
import pathlib

class GeminiKeywordGenerator(object):
    def __init__(
            self,
            model_name = "gemini-1.5-pro",
            temperature = 0.1,
            top_p = 1,
            top_k = 1,
            max_out_tokens = 2048 
            ) -> None:
        try:
            path_env = pathlib.Path(os.getcwd()) / '.env'
            load_dotenv(path_env)
            gemini_api_key = os.getenv("GEMINI_API_KEY")
            genai.configure(api_key=gemini_api_key)
        except KeyError:
            raise Exception(
                "Please set the GEMINI_API_KEY environment variable."
            )
        
        # Set up the model
        generation_config = {
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "max_output_tokens": max_out_tokens,
            }

        safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        ]

        self.model = genai.GenerativeModel(model_name=model_name,
                                      generation_config=generation_config,
                                      safety_settings=safety_settings)
    def get_kwds(self, cat:str, num_kwds:int)-> str:
        convo = self.model.start_chat(history=[
            {
                "role": "user",
                "parts": ["essay on ai"]
            },
            {
                "role": "model",
                "parts": ["**Artificial Intelligence: A Paradigm Shift**\n\nArtificial intelligence (AI) has emerged as a transformative force in contemporary society, reshaping industries, redefining work, and blurring the lines between human and machine capabilities. This essay delves into the profound implications of AI, exploring its potential benefits and challenges while considering its impact on the future of humanity.\n\n**Benefits of AI**\n\nOne of the most significant benefits of AI is its ability to automate tasks, freeing up human workers for more complex and fulfilling endeavors. AI-powered systems can perform mundane and repetitive tasks with precision and efficiency, enabling businesses to optimize their operations and reduce costs. This has led to increased productivity and economic growth across various sectors.\n\nFurthermore, AI has proven invaluable in solving complex problems. Machine learning algorithms can analyze vast amounts of data to identify patterns and make predictions that assist in decision-making. For instance, AI systems are used in healthcare to diagnose diseases, predict patient outcomes, and develop personalized treatment plans.\n\nAI also has the potential to improve accessibility and equality. By automating routine tasks and providing personalized experiences, AI can help break down barriers for individuals with disabilities or limited access to resources. For example, AI-powered assistive technologies enable people with physical impairments to interact with the world more effectively.\n\n**Challenges of AI**\n\nWhile AI offers immense promise, it also presents several significant challenges. One of the most pressing concerns is the potential for job displacement. As AI becomes more sophisticated, it could automate tasks currently performed by human workers, leading to job losses in certain industries.\n\nAnother challenge is the ethical implications of AI. As AI systems become increasingly autonomous, questions arise about their moral agency and accountability. For instance, if an AI-powered self-driving car causes an accident, who is responsible: the driver, the manufacturer, or the programmer?\n\nMoreover, AI-powered systems are prone to biases if the data they are trained on is biased. This can result in unfair or discriminatory decisions, exacerbating existing social inequalities. It is essential to address these biases through proper data collection and algorithmic transparency.\n\n**Impact on the Future**\n\nAI is expected to continue to play an increasingly prominent role in our lives in the years to come. It has the potential to transform industries, disrupt existing business models, and create entirely new economic opportunities. As AI becomes more advanced, it could lead to breakthroughs in fields such as healthcare, transportation, and manufacturing.\n\nThe future of AI-human interaction is also uncertain. As AI systems become more intelligent, there is a possibility that they could develop their own consciousness and agency. This raises questions about the relationship between humans and machines and the ethical implications of creating artificial beings.\n\n**Conclusion**\n\nArtificial intelligence is a powerful technology with the potential to both benefit and challenge humanity. Its benefits include increased productivity, improved problem-solving capabilities, and enhanced accessibility. However, it also poses challenges such as job displacement, ethical dilemmas, and biases. As AI continues to evolve, it is imperative to navigate these challenges thoughtfully and ensure that this transformative technology is used for the betterment of society.\n\nBy harnessing the potential of AI while mitigating its risks, we can create a future in which humans and machines collaborate harmoniously, unlocking unprecedented opportunities for progress and prosperity. The development and deployment of AI must be guided by ethical principles, ensuring that it is deployed responsibly and for the benefit of all."]
            },
            ])
        convo.send_message(f"A python dictionary with the {num_kwds} most relevant keywords related with '{cat}' along with their importance weight (from 0 to 10). Do not include the word itself.")
        return convo.last.text
    
    #def get_dictionary( )




