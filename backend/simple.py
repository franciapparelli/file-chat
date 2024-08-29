import os
import google.generativeai as genai
import PIL.Image

os.environ["GOOGLE_API_KEY"] = "AIzaSyDAX_9KcqA3vkHdbWm6q4AuznZ3J8V0xbM"

genai.configure()
# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
)

mis_imagenes = [PIL.Image.open("vaticano.jpeg"), PIL.Image.open("gijon.jpg")]

# TODO Make these files available on the local file system
# You may need to update the file paths   
prompt = input("")
response = model.generate_content([prompt, mis_imagenes[0], mis_imagenes[1]])
print(response.text)