"""
to setup python environment with needed packages:
conda create -n openai-cloud 
conda activate openai-cloud 
conda install -c conda-forge openai>=1.2.4 ipykernel jupyterlab notebook python=3.10.0  

to set up kernel in jupyterlabs:  

python -m ipykernel install --user --name=openai-cloud 

reference: 
https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety
"""


from openai import OpenAI
import base64
import json
import os
from urllib.parse import urlparse

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def process_response(response):
    json_string = response.choices[0].message.content
    json_string = json_string.replace("```json\n", "").replace("\n```", "")
    json_data = json.loads(json_string)

    #filename_without_extension = os.path.splitext(os.path.basename(urlparse(base64_img).path))[0] #for URL image
    filename_without_extension = os.path.splitext(os.path.basename(image_local))[0] #for local image

    json_filename = f"{filename_without_extension}.json"
    with open("./Data/" + json_filename, 'w') as file:
        json.dump(json_data, file, indent=4)
    print(f"JSON data saved to {json_filename}")

# image_local = 'ML-1955-2.png'
image_local = 'dl1.png'
base64_img = f"data:image/png;base64,{encode_image(image_local)}"
#image_url = 'https://d2908q01vomqb2.cloudfront.net/f1f836cb4ea6efb2a0b1b99f41ad8b103eff4b59/2021/02/19/ML-1955-2.jpg'

client = OpenAI() #Best practice needs OPENAI_API_KEY environment variable
# client = OpenAI('OpenAI API Key here')

response = client.chat.completions.create(
    model='gpt-4o',
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Return JSON document with data. Only return JSON not other text"},
                {
                    "type": "image_url",
                    # for online images
                    # "image_url": {"url": image_url}
                    "image_url": {"url": f"{base64_img}"}
                }
            ],
        }
    ],
    max_tokens=500,
)

process_response(response)

