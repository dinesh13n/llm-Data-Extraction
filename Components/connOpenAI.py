import openai
from langchain.chat_models import ChatOpenAI
import os


class moduleOpenAI():

    def __init__(self,log,ConfigDict):
        # Read config file to get the parameter value
        self.log = log # Initiate log object to capture the appliation log
        self.config_Data = ConfigDict["OPENAI"]
        #print(self.config_Data)# Read the OPENAI parameters from the Config file
        os.environ["OPENAI_API_KEY"]=self.config_Data["OPENAI_API_KEY"] # Get the OPENAI_API_KEY to set the environment

        # Get remaining OPENAI parameter from the config file
        self.model_name = self.config_Data["OPENAI_TEXT_MODEL"]
        self.temperature = self.config_Data["OPENAI_TEMP"]

    def textGPTModel(self):

        try:
            # Create object for OPENAI llm model
            llm_model = ChatOpenAI(
                model_name = self.model_name,
                temperature = self.temperature
            )
        except Exception as e:
            self.log.critical("Unable to create llm model object with exception - ",e)

        return llm_model