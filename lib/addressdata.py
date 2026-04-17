#imports
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
client = OpenAI()

import requests
from bs4 import BeautifulSoup


# --------------------------------------------------------------------


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
    Return the information as a single string. Keep it short (approx 150 words)

    """

    response = client.responses.create(
        model="gpt-5-nano",
        input= prompt) 

    results = response.output_text


    return results
    
# 🔗 url checker

def check_url(urls):

    results = []

    for url in urls:
        
        print(f"Checking URL: {url}")

        prompt = f"""
        Extract information from the URL that would be useful for understanding the specific address and local area. 
        Prioritise information about the specific address listed where possible

        The URL is: {url}

        Use the URL as a header for the information.
        Return the information as a single string. Keep it short (approx 100 words)

        """

        response = client.responses.create(
            model="gpt-5-nano",
            input= prompt) 

        results.append(response.output_text)


    return results



if __name__ == "__main__":

    address = "198 Church St, Parramatta, NSW, Australia"

    urls = [
        "https://www.realestate.com.au/property/198-church-st-parramatta-nsw-2150/",
        "https://www.google.com/maps/place/198-church-st-parramatta-nsw-2150/"
        ]

    census_url = "https://www.abs.gov.au/census/find-census-data/quickstats/2021/125"

    output =[]

    print("Running address data check...")

    output.append(check_url(urls))
    output.append(check_census(census_url))

    print(output)