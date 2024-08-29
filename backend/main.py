from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
import os
from fastapi.middleware.cors import CORSMiddleware

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

chat_session = model.start_chat(
  history =
  [
    {
      "role": "user",
      "parts": ""
    }
  ]
)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserMessage(BaseModel):
    input: str    

@app.get("/")
async def root():
    return "HOLA DESDE ROOT"

@app.post("/users")
async def users(data: UserMessage):
    response = chat_session.send_message(data.input)
    return f"{response.text}"