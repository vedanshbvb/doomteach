import sys
from openai import OpenAI

shapes_client = OpenAI(
    api_key="A2WHR9GRSEPOTJKG9XOKX76EZ8PN9VIRGHEQ9CZVY3W",
    base_url="https://api.shapes.inc/v1/",
)

def generate_script(user_prompt):
    print("generating script")
    response = shapes_client.chat.completions.create(
        model="shapesinc/jsonbot",
        messages=[
            {
                "role": "user",
                "content": f"""
                You are a script writer for a social media reel and you possess great knowledge of popular culture and iconic characters and also are a very skilled tech enthusiast.
                User will give you a command for writing a short, engaging script for a reel featuring two iconic characters which will be given to you in the command. The theme of the reel is a discussion about some topic which will be given to you in the command. The script should be full of knowledge about the topic and be suitable for a quick, entertaining video format, around 1 to 2 minutes. One of the characters should be asking questions and the other should be answering them. 
                The speaker of the dialogue should be in double quotes and the dialogue should come after a colon. The dialogue should also be in double quotess. The output should be a json object. Make sure the script starts with curly brackets and also ends with curly brackets. For example :

            
                {{
                "Stewie": "How are you?",
                "Peter": "I am fine, thank you!",
                "Stewie": "Awesome!"
                }}


                Command: {user_prompt}
                Output a json object starting and ending with curly brackets.
                """
            }
        ]
    )
    script = response.choices[0].message.content.strip()
    return script

def identify_characters(user_prompt):
    print("Identifying characters")
    response = shapes_client.chat.completions.create(
        model="shapesinc/reelscripter",
        messages=[
            {
                "role": "user",
                "content": f"""
                Identify the characters in the following command and return their names. You should only return the names of the characters in a comma separated format. Do not return any other text or explanation. 
                For eg: "Write a script for Obama and Trump where they discuss about Kubernetes" should return "Barack Obama, Donald Trump"

                Command: {user_prompt}
                """
            }
        ]
    )
    characters = response.choices[0].message.content.strip()
    return characters

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script_generator.py '<user_prompt>'")
        sys.exit(1)
    user_prompt = sys.argv[1]
    script = generate_script(user_prompt)
    print("Generated Script:\n" + script)
    characters = identify_characters(user_prompt)
    print("Identified Characters: " + characters)

