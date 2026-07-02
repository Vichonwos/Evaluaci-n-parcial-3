from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(
    title="Microservicio DOY0101",
    description="Microservicio base para pipeline CI/CD - Ingeniería DevOps",
    version="1.0.0"
)

# Activar el "megáfono" de métricas para Prometheus
Instrumentator().instrument(app).expose(app)

# Constantes

# Constantes
ITEM_NOT_FOUND = "Item no encontrado"


# Modelo de datos
class Item(BaseModel):
    id: Optional[int] = None
    nombre: str
    descripcion: str
    precio: float

# Base de datos simulada en memoria
items_db: List[Item] = []
counter = 1


@app.get("/")
def root():
    return {"mensaje": "Microservicio activo", "version": "1.0.0"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/items", response_model=List[Item])
def listar_items():
    return items_db


@app.get("/items/{item_id}", response_model=Item, responses={404: {"description": ITEM_NOT_FOUND}})
def obtener_item(item_id: int):
    for item in items_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail=ITEM_NOT_FOUND)


@app.post("/items", response_model=Item, status_code=201)
def crear_item(item: Item):
    global counter
    item.id = counter
    counter += 1
    items_db.append(item)
    return item


@app.put("/items/{item_id}", response_model=Item, responses={404: {"description": ITEM_NOT_FOUND}})
def actualizar_item(item_id: int, item_actualizado: Item):
    for i, item in enumerate(items_db):
        if item.id == item_id:
            item_actualizado.id = item_id
            items_db[i] = item_actualizado
            return item_actualizado
    raise HTTPException(status_code=404, detail=ITEM_NOT_FOUND)


@app.delete("/items/{item_id}", responses={404: {"description": ITEM_NOT_FOUND}})
def eliminar_item(item_id: int):
    for i, item in enumerate(items_db):
        if item.id == item_id:
            items_db.pop(i)
            return {"mensaje": f"Item {item_id} eliminado"}
    raise HTTPException(status_code=404, detail=ITEM_NOT_FOUND)
