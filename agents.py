#Agents functions 

#imports
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
client = OpenAI()


# --------------------------------------------------------------------


# 👓 Vision Agent

def vision_agent(images):
    response = client.responses.create(
        model="gpt-4.1", 
        input=[{
            "role": "user",
            "content": [
                {"type": "input_text", "text": "Analyse these urban images..."},
                *[
                    {"type": "input_image", "image_url": img}
                    for img in images
                ]
            ]
        }],
        response_format={
            "type": "json_schema",
            "json_schema": {...}
        }
    )
    return response.output_parsed


# --------------------------------------------------------------------

# 👤 Context Agent

def context_agent(data):

    prompt = f"""
    Analyse the following reviews and place data...
    Extract vibe, activity level, and granular uses.
    """



# --------------------------------------------------------------------

# 🔗 Synthesis Agent

def synthesis_agent(inputs):

    prompt = f"""
    You are an urban analyst.

    Combine:
    - Vision data: {inputs['vision']}
    - Context data: {inputs['context']}

    Resolve conflicts and produce a NARRATIVE SUMMARY of the urban intelligence. 
    Use the heading "NARRATIVE SUMMARY" and aim for 2-3 paragraphs at approximately 200 words.

    Following the NARRATIVE SUMMARY, produce a JSON object labelled "URBAN DNA" with the following keys:

    Height Range: 
    Dominant Use:     
    Primary Typology: 
    Material Palette: 
    Activity Level:   
    Style:            
    Confidence: 


    """

    response = client.responses.create(
        model="gpt-5-nano",
        input= prompt
    )

    return response