#Agents functions 

#imports
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
client = OpenAI()

import requests
from bs4 import BeautifulSoup


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


    Analyse the following reviews and extract:

    - Overall sentiment (0 to 1)
    - Common descriptors (e.g. lively, quiet, touristy)
    - Activity patterns (day vs night)
    - Dominant place types (cafe, bar, retail)
    - Any indicators of noise, crowding, or atmosphere

    """



# Place agent

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
        Return the information as a structured json object. 

        The json object should have the following keys:
        - URL source
        - Insights (i.e AI generated insights about the place)

        """

        response = client.responses.create(
            model="gpt-5-nano",
            input= prompt) 

        results = response.output_text

        return results
        

    #     - URL source
    #     - Total Population
    #     - Gender Mix
    #     - Median Age
    #     - Age Mix Profile
    #     - Indegenous Status
    #     - Income
    #     - Education
    #     - Employment
    #     - Housing
    #     - Ancestry
    #     - Dwelling types
    #     - Language
    #     - Insights (i.e AI generated insights about the place)




    # 🔗 url checker

    def check_url(urls):

        results = {}

        for url in urls:
            
            print(f"Checking URL: {url}")

            prompt = f"""
            Extract information from the URL that would be useful for understanding the specific address and local area. 
            Prioritise information about the specific address listed where possible

            The URL is: {url}

            Return the information as a structured json object.
            The json object should have the following keys:
            - URL source
            - Specific address
            - Suburb
            - Postcode
            - Area Description
            - Local area context
            - Transporatation
            - Insights (i.e AI generated insights about the place)

            """

            response = client.responses.create(
                model="gpt-5-nano",
                input= prompt) 

            results[url] = response.output_text

        return results


    address = "198 Church St, Parramatta"

    urls = [
        "https://www.realestate.com.au/property/198-church-st-parramatta-nsw-2150/",
        "https://www.google.com/maps/place/198-church-st-parramatta-nsw-2150/"
        ]

    census_url = "https://www.abs.gov.au/census/find-census-data/quickstats/2021/125"

    output ={}

    print("Running address data check...")

    output['url_data'] = check_url(urls)
    output['census_data'] = check_census(census_url)

    return output



# --------------------------------------------------------------------

# 🔗 Synthesis Agent

def synthesis_agent(inputs):

    prompt = f"""
    You are an urban analyst.

    Combine:
    - Vision data:
    - Place data: 

    Resolve conflicts and produce a NARRATIVE SUMMARY of the urban intelligence. 
    Use the heading "NARRATIVE SUMMARY" and aim for approximately 300 words.

    Following the NARRATIVE SUMMARY, produce a JSON object labelled "URBAN DNA" with the following keys:

    Height Range: 
    Dominant Use:     
    Primary Typology: 
    Material Palette: 
    Activity Level:   
    Style:            
    Confidence: 
    Demographics:
    Insights: (i.e AI generated insights about the place)

    """

    response = client.responses.create(
        model="gpt-5-nano",
        input= prompt
    )

    return response


if __name__ == "__main__":
    print(place_agent())

    