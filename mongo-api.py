from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from datetime import datetime
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

#client = MongoClient(os.environ["MONGO_URI"])
client = MongoClient("mongodb://ISIS2304D20202610:GPpXjA8nX7lk@157.253.236.88:8087")  
db = client["ISIS2304D20202610"]

eventos = db["eventos"]
comentarios = db["comentarios"]


@app.get("/")
def inicio():
    return {"estado": "API funcionando correctamente"}

@app.get('/bares/{bar_id}/comentarios')
def get_comentarios(bar_id: int):
    comentarios = list(comentarios.find({"bar_id":bar_id}, {"_id":0}))    
    return comentarios

@app.post('/bares/{bar_id}/comentarios')
def post_comentario(bar_id: int, datos: dict):
    datos['bar_id'] = bar_id
    datos['fecha']  = datetime.now().isoformat()
    comentarios.insert_one(datos)
    return {'mensaje': 'Comentario guardado'}

@app.get('/bares/{bar_id}/eventos')
def get_eventos(bar_id: int):
    eventos = list(eventos.find({"bar_id": bar_id}, {"_id":0}))
    return eventos

@app.post('/bares/{bar_id}/eventos')
def post_eventos(bar_id: int, datos: dict):
    datos['bar_id'] = bar_id
    datos['fecha_creacion'] = datetime.now().isoformat()
    eventos.insert_one(datos)
    return{'mensaje': 'Evento guardado'}
