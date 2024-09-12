# Comando para instalar gemini: pip install google-generativeai

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

import os
import google.generativeai as genai

os.environ["GOOGLE_API_KEY"] = "AIzaSyBp1RVo7MwQdrJsFxxMBUOK5XYxAVmTgKA"

genai.configure()

model = genai.GenerativeModel("gemini-1.5-flash")

# TODO Make these files available on the local file system
# You may need to update the file paths

def messagesGemini(message):
    response = model.generate_content(message, stream=True)
    response.resolve()
    return response.text

def insert_mensaje(conn, chatId, userId, content):
    try:
        sql_insert = """
        INSERT INTO Messages (chatId, userId, content)
        VALUES (?, ?, ?);
        """
        cursor = conn.cursor()
        cursor.execute(sql_insert, (chatId, userId, content))
        conn.commit()
        print("Mensaje insertado exitosamente.")
    except Exception as e:
        print(f"Error al insertar el mensaje: {e}")
    finally:
        if conn:
            conn.close()  # Cierra la conexión
 
def insert_mensajeAI(conn, chatId, content):
    try:
        sql_insert = """
        INSERT INTO Messages (chatId, userId, content)
        VALUES (?, ?, ?);
        """
        userId = 3 # 3 porque es el id del system
        cursor = conn.cursor()
        cursor.execute(sql_insert, (chatId, userId, content))
        conn.commit()
        print("Mensaje AI insertado exitosamente.")
    except Exception as e:
        print(f"Error al insertar el mensaje AI: {e}")
    finally:
        if conn:
            conn.close()  # Cierra la conexión

def get_messages(conn, userId, chatId):
    try:
        sql_select = """
        SELECT * FROM tabla_chat WHERE userId = ? AND chatId = ?;
        """
        cursor = conn.cursor()
        cursor.execute(sql_select, (userId, chatId))
        resultados = cursor.fetchall()
       
        return resultados
    except Exception as e:
        print(f"Error al insertar el mensaje: {e}")
    finally:
        if conn:
            conn.close()  # Cierra la conexión