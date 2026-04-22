#Agents functions 

#imports
from dotenv import load_dotenv
from pydantic import Json
load_dotenv()

from openai import OpenAI
client = OpenAI()

import requests
from bs4 import BeautifulSoup
import base64  
from pathlib import Path
import os
import json

from lib.vision_prompt import analyse_img_prompt







# --------------------------------------------------------------------


# 👓 Vision Agent

# Function to encode local image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')






# Function to process images
def vision_agent(images):
    ROOT_DIR = Path(__file__).parent
    json_filepath = ROOT_DIR / "image_response.json"


    # Encode images
    encoded_images = [encode_image(img) for img in images]

    print(encoded_images[0])
    print("\n\n",analyse_img_prompt)



    response = client.responses.create(
        model="gpt-4.1", 
        input=[{
            "role": "user",
            "content": [
                {"type": "input_text", "text": analyse_img_prompt},

                *[{"type": "input_image", "image_url": f"data:image/jpeg;base64,{img_b64}"}
                    for img_b64 in encoded_images]

            ]
        }],
    )

    with open(json_filepath, 'w') as f:
        json.dump(response.output_text, f, indent=4)

    return response


# --------------------------------------------------------------------

# 👤 Context Agent

def vibe_agent(data):

    prompt = f"""
    Analyse the following reviews and place data...
    Extract vibe, activity level, and granular uses.


    Analyse the following reviews and extract:

    - Overall sentiment (0 to 1)
    - Common descriptors (e.g. lively, quiet, touristy)
    - Activity patterns (day vs night)
    - Dominant place types (cafe, bar, retail)
    - Any indicators of noise, crowding, or atmosphere

    """


# --------------------------------------------------------------------
# 📊 Place agent

def place_agent():

    # 📊 census checker
    def check_census(url):


        url_response = requests.get(url)
        soup = BeautifulSoup(url_response.text, 'html.parser')
        results = soup.get_text(separator=' ', strip=True) 


        print("Checking census data....")

        prompt = f"""
        Extract relevant census nformation from text provided. Focus on key demographics such as geneder, age, income, education, employment, housing, and population.
        

        The text is: {results}

        Use the URL as a header for the information.
        Return generated insights about the place based on the census data.

        """

        response = client.responses.create(
            model="gpt-5-nano",
            input= prompt) 

        results = response.output_text

        return results
        

    # 🔗 url checker

    def check_url(urls):

        results = {}

        for url in urls:
            
            print(f"Checking URL: {url}")

            prompt = f"""
            Extract information from the URL that would be useful for understanding the specific address and local area. 
            Prioritise information about the specific address listed where possible

            The URL is: {url}

            Use the URL as a header for the information.
            Return generated insights about the place based on the URL information. Keep the response to approximately 100-200 words
            """

            response = client.responses.create(
                model="gpt-5-nano",
                input= prompt) 

            results[url] = response.output_text

        return results


    address = "31 Macquarie Street, Parramatta"

    urls = [
        "https://www.realestate.com.au/property/31-macquarie-street-parramatta-nsw-2150/",
        "https://www.realestate.com.au/property/l3-35-macquarie-st-parramatta-nsw-2150/"
        ]

    census_url = "https://www.abs.gov.au/census/find-census-data/quickstats/2021/125"

    output ={}

    print("Running address data check...")

    output['url_data'] = check_url(urls)
    output['census_data'] = check_census(census_url)

    return output

# --------------------------------------------------------------------

# ❓ Pattern agent

def pattern_agent(data):


    prompt = f"""
    Analyse the following data. Identify patterns that are present in the pixel values of the images. The insights should be creative and 
    interesting and ideally not obvious to a human observer. For example you could review information about the pixel values, metadata etc.  
   
    Your response should be generated insights about patterns occuring within the image data set. Keep the response to approximately 100-200 words

    The data is: {data}
    """


    response = client.responses.create(
                model="gpt-5-nano",
                input= prompt) 


    results = response.output_text

    return results

# --------------------------------------------------------------------

# 🔍 Insights agent

def insights_agent(data):
    prompt = f"""
    Analyse the following data. Act as an expert urban analyst. Your task is to identify accessibility concerns and opportunities within the image data set. 
    For example crime prevention through environmental design (CPTEC) opportunities and concerns. Concerns around accessibility, disability, visibility, lighting,
     noise, and other factors.
    
    Your response should include the following information. Keep the response to approximately 100-200 words
    - CPTED (Crime Prevention Through Environmental Design) Opportunities and Concerns
    - Accessibility Opportunities and Concerns
    - Insights (i.e AI generated insights about patterns occuring within the image data set)

    The data is: {data}
    """

    
    response = client.responses.create(
                model="gpt-5-nano",
                input= prompt) 


    results = response.output_text

    return results



# --------------------------------------------------------------------

# 🔗 Synthesis Agent

def synthesis_agent(inputs):

    prompt = f"""
    You are an urban analyst.

    Combine:
    - Vision data / Visual summary: {inputs['vision']}
    - Place / Context data: {inputs['place']}
    - Multi-Image Pattern data: {inputs['pattern']}
    - Accessibility and Insights data: {inputs['insights']}


    Resolve conflicts and produce a NARRATIVE SUMMARY of the urban intelligence. 
    Use the heading "NARRATIVE SUMMARY". Include a paragraph for each of the following sections: 
    
    VISUAL SUMMARY, PLACE / CONTEXT INFORMATION, MULTI-IMAGE PATTERN ANALYSIS, ACCESSIBILITY AND INSIGHTS.

    Aim for approximately 100 words for each section.


    Following the NARRATIVE SUMMARY, include a section called "RECOMMENDATIONS" which includes a dot point list of AI design recommendations 
    for the place based on the data. 
    
    
    Following the RECOMMENDATIONS, produce a JSON object labelled "URBAN DNA" with the following keys:

    Insights: (i.e AI generated insights about the place)
    Height Range: 
    Dominant Use:     
    Primary Typology: 
    Material Palette: 
    Activity Level:   
    Style:            
    Detected elements: (i.e list of clearly visible elements in the vision data)
    Confidence: 
    Demographics: (including income, education, employment, housing, population etc)
    Aggregate Scores: As defined in the vision data 

    """

    response = client.responses.create(
        model="gpt-5-nano",
        input= prompt
    )

    return response


if __name__ == "__main__":

    print("Hello World")

    # print(place_agent())









