from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from communication.router import router


app = FastAPI()


app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],

)

app.include_router(router)  

@app.get("/model/current")
def get_current_model():

    return engine.get_current_model()