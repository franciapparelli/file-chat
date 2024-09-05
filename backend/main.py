from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.users import routes as users_routes
from routers.chats import routes as chats_routes
from routers.messages import routes as messages_routes

app = FastAPI()

app = FastAPI(
    title="Your API Title",
    description="Your API Description",
    version="1.0.0",
    openapi_tags=[
        {"name": "users", "description": "Operations related to users"},
        {"name": "tasks", "description": "Operations related to tasks"},
    ],
)

origins = [
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
    )

# Incluir routers
app.include_router(users_routes.router, prefix="/users", tags=["users"])
app.include_router(chats_routes.router, prefix="/chats", tags=["chats"])
app.include_router(messages_routes.router, prefix="/messages", tags=["messages"])

# Ruta de prueba
@app.get("/")
async def read_root():
    return {"message": "Hello World"}
