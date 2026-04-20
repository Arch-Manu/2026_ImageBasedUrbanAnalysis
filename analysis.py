from agents import *
import json


if __name__ == "__main__":

    # -------------------------------------
    # Load images
    # -------------------------------------

    ROOT_DIR = Path(__file__).parent
    IMG_DIR = ROOT_DIR / "images"


    images = []

    for file in os.listdir(IMG_DIR):
        if file.endswith(('.JPG', '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')):
            images.append(os.path.join(IMG_DIR, file))


    # -------------------------------------
    # Vision Agent 
    # -------------------------------------

    print("\nVision Agent analysing images…\n")

    #load vision data from file
    
    # with open('vision_example.json', 'r', encoding='utf-8') as file:
    #     vision_example = json.load(file)


    #send to OpenAI API
    vision_data = vision_agent(images)
    print("VISION DATA:\n", vision_data)


    # -------------------------------------
    # Pattern Agent 
    # -------------------------------------

    print("\nPattern Agent analysing pattern data…\n")
    pattern_data = pattern_agent(vision_data)
    print("PATTERN DATA:\n", pattern_data)

    # -------------------------------------
    # Insights Agent 
    # -------------------------------------

    print("\nInsights Agent analysing insights data…\n")
    insights_data = insights_agent(vision_data)
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
        "vision": vision_data,
        "place": place_data,
        "pattern": pattern_data,
        "insights": insights_data
    })

    
    output_message = final.output_text

    print("\n" + str(output_message))
