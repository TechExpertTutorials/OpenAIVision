import base64
import requests
import os

# Replace with your OpenAI API key
# api_key = "YOUR_OPENAI_API_KEY"
api_key = os.environ['OPENAI_API_KEY']

# Replace with the image path you want to extract text from
image_path = 'dl1.png'

def encode_image(image_path):
  """
  Encodes an image file to base64 string
  """
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def extract_text(image_data):
  """
  Extracts text from an image using OpenAI Vision
  """
  headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {api_key}"
  }
  payload = {
      "model": "gpt-4o",
      "messages": [
          {
              "role": "user",
              "content": [
                  {
                      "type": "text",
                      "text": "What is the text in this image?"
                  },
                  {
                      "type": "image_url",
                      "image_url": {"url": f"data:image/png;base64,{image_data}"}
                  }
              ]
          }
      ]
  }
  response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
  response_data = response.json()
  if "choices" in response_data and len(response_data["choices"]) > 0:
    return response_data["choices"][0]["message"]["content"].strip()
  else:
    return "Could not extract text from image."

# Encode the image to base64
image_data = encode_image(image_path)

# Extract text using OpenAI Vision
extracted_text = extract_text(image_data)

# Print the extracted text
print(extracted_text)