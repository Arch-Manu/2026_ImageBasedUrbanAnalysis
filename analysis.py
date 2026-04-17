from agents import *
import json


if __name__ == "__main__":


    # -------------------------------------
    # Vision Agent 
    # -------------------------------------

    print("\nVision Agent analysing images…\n")
    with open('vision_example.json', 'r', encoding='utf-8') as file:
        vision_example = json.load(file)
    # print(vision_example)

    
    # -------------------------------------
    # Place Agent 
    # -------------------------------------

    print("\nPlace Agent analysing place data…\n")
    place_data = place_agent()
    # print(place_data)
   


    # -------------------------------------
    # Synthesis Agent
    # -------------------------------------

    print("\nSynthesising urban intelligence…\n")
    final = synthesis_agent({
        "vision": vision_example,
        "place": place_data
    })

    
    output_message = final.output_text

    print("\n" + str(output_message))
