from agents import *
import json


if __name__ == "__main__":


    # -------------------------------------
    # Vision Agent 
    # -------------------------------------

    print("\nVision Agent analysing images…\n")
    with open('vision_example.json', 'r', encoding='utf-8') as file:
        vision_example = json.load(file)
    print("VISION EXAMPLE:\n", vision_example)


    # -------------------------------------
    # Pattern Agent 
    # -------------------------------------

    print("\nPattern Agent analysing pattern data…\n")
    pattern_data = pattern_agent(vision_example)
    print("PATTERN DATA:\n", pattern_data)

    # -------------------------------------
    # Insights Agent 
    # -------------------------------------

    print("\nInsights Agent analysing insights data…\n")
    insights_data = insights_agent(vision_example)
    print("INSIGHTS DATA:\n", insights_data)


    # -------------------------------------
    # Place Agent 
    # -------------------------------------

    print("\nPlace Agent analysing place data…\n")
    place_data = place_agent()
    print("PLACE DATA:\n", place_data)
   


    # -------------------------------------
    # Synthesis Agent
    # -------------------------------------

    print("\nSynthesising urban intelligence…\n")
    final = synthesis_agent({
        "vision": vision_example,
        "place": place_data,
        "pattern": pattern_data,
        "insights": insights_data
    })

    
    output_message = final.output_text

    print("\n" + str(output_message))
