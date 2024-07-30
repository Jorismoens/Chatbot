from prompts import PROMPTS
from src.callAsistant import callAsistantWithTools
from src.tools.toolSchemas import tryRandomNTool, temperatureTool

# Provide the model with helper functions to ask the temperature and to generate random numbers
tools = [
    tryRandomNTool,
    temperatureTool
]

print(callAsistantWithTools(tools,
                            "You assist me with calling specific tools to retrieve the temperature or generate " \
                            "random numbers.",
                            prompt=PROMPTS["bbqWeather"]))
