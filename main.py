# Import Library
from datetime import datetime
from kor.extraction import create_extraction_chain
from application_logging.AppLogging import AppLog
from Components.readConfigFile import Read_Config_File
from Components.promptTemplate import llmTemplates
from Components.connOpenAI import moduleOpenAI
from fastapi import FastAPI, status, Depends, Response
from fastapi.exceptions import HTTPException

import re
import warnings
warnings.filterwarnings("ignore")
import uvicorn


app = FastAPI()
# uvicorn main:app --reload

# ---------- Start Create Objects -----------------

# datetime object containing current date and time
now = datetime.now()
# dd/mm/YY H:M:S
dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")

# Create object for Application Logging
exeType = "Application"
applog = AppLog(exeType,logfile=dt_string+".log")
log = applog.log("sLogger")

# Create object to read config json file
objReadConfigFile = Read_Config_File(log,".//config.json")

# ------------End Create Objects---------------------------

#--------------------- Start Object Initiation Process------------

# Read config file to execute application
FileStatus, ConfigDict = objReadConfigFile.readData()
if FileStatus == 1:  # 1 - Successfully read file, 0 - Failed to read file

    # Create object to get llm template
    objTemplate = llmTemplates(log=log)

    # Create object to get OpenAI llm object
    objllm = moduleOpenAI(log=log, ConfigDict=ConfigDict)

    # Get prompt template schema
    schema = objTemplate.cat_int_sent_template()

    # Get the llm object
    llm = objllm.textGPTModel()

else:
    log.critical("Unable to read config file, please check the log file")
    Failed_Message = "Unable to read config file, please check the log file"


#--------------------- End Object Initiation Process------------

@app.get("/getInfo/{inpText}", status_code=status.HTTP_200_OK)
# Extract the Category, Intent and Sentiment from the sentance
async def get_CatIntSent_Info(inpText: str, response: Response):

    #
    if FileStatus == 1 and inpText.isnumeric() == False and re.sub(r"\s+","",inpText) != "\"\"":

        # get chain object with open ai model
        chain = create_extraction_chain(llm, schema)
        #print(chain.prompt.format_prompt(text="[user input]").to_string())

        return chain.predict_and_parse(text=inpText)["data"]['sentence_info'][0]

    else:
        if FileStatus == 1:
            Failed_Message = "Only string message is allowed"

        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=Failed_Message)


# if __name__ == '__main__':
#     uvicorn.run(app=app, host="127.0.0.1", port=8000)