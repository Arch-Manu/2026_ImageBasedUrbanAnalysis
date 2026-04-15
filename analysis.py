from agents import *
import json


def run_analysis(input_data):
    
    print("Vision Agent analysing images…")
    vision = vision_agent(input_data["images"])
    
    print("Context Agent reading reviews…")
    context = context_agent(input_data["location"])
    
    print("Synthesising urban intelligence…")
    final = synthesis_agent({
        "vision": vision,
        "context": context
    })
    
    return final






if __name__ == "__main__":

    # run_analysis(data)

    #SYNTHETIC DATASET TEST

    with open('synthetic_input.JSON', 'r', encoding='utf-8') as file:
        synthetic_input = json.load(file)


    print("\nVision Agent analysing images…\n")
    print(synthetic_input["vision"])

    print("\nContext Agent reading reviews…\n")
    print(synthetic_input["context"])
    
    print("\nSynthesising urban intelligence…\n")
    final = synthesis_agent({
        "vision": synthetic_input["vision"],
        "context": synthetic_input["context"]
    })

    
    output_message = final.output_text

    print("\n" + str(output_message))
