# import os
# import google.generativeai as genai
# import PIL.Image

# os.environ["GOOGLE_API_KEY"] = "AIzaSyDAX_9KcqA3vkHdbWm6q4AuznZ3J8V0xbM"

# genai.configure()

# # Create the model
# generation_config = {
#   "temperature": 1,
#   "top_p": 0.95,
#   "top_k": 64,
#   "max_output_tokens": 8192,
#   "response_mime_type": "text/plain",
# }

# model = genai.GenerativeModel(
#   model_name="gemini-1.5-flash",
#   generation_config=generation_config,
#   # safety_settings = Adjust safety settings
#   # See https://ai.google.dev/gemini-api/docs/safety-settings
# )

# # TODO Make these files available on the local file system
# # You may need to update the file paths

# mi_pdf = genai.upload_file(path="Phrasal_Verbs_Vince.pdf", display_name="codigo_penalPDF")
# pdf = genai.get_file(name=mi_pdf.name)

# chat_session = model.start_chat(
#   history =
#   [
#     {
#       "role": "user",
#       "parts": "Mi nombre es Franco"
#     }
#   ]
# )

# for file in genai.list_files():
#   print(f"{file.display_name}, URI: {file.uri}")

# # while True:
# #   prompt = input("")
# #   response = chat_session.send_message([prompt, pdf])
# #   print(response.text)
