from fastapi import FastAPI
from routers.users import routes as users_routes
from routers.chats import routes as chats_routes
from routers.messages import routes as messages_routes

app = FastAPI()

# Incluir routers
app.include_router(users_routes.router, prefix="/users", tags=["users"])
app.include_router(chats_routes.router, prefix="/chats", tags=["chats"])
app.include_router(messages_routes.router, prefix="/messages", tags=["messages"])

# Ruta de prueba
@app.get("/")
async def read_root():
    return {"message": "Hello World"}
