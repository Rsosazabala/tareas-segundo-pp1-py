from fastapi import Body, FastAPI, Path, Query

app = FastAPI()

app.title = "API de articulos de futbol"

articulos = [
    {"id": 1, "nombre": "Pelota Adidas", "precio": 15000, "activo": True},
    {"id": 2, "nombre": "Botines Nike", "precio": 45000, "activo": True},
    {"id": 3, "nombre": "Camiseta Seleccion", "precio": 30000, "activo": True},
]


@app.get("/articulos")
async def ver_articulos():
    return [a for a in articulos if a["activo"]]


@app.get("/articulos/{id}")
async def ver_articulo_por_id(
    id: int = Path(gt=0, description="Id del articulo > 0")
):
    for articulo in articulos:
        if articulo["id"] == id:
            return articulo
    return {"mensaje": "Articulo no encontrado"}


@app.post("/articulos")
async def agregar_articulo(
    id: int = Body(gt=0),
    nombre: str = Body(min_length=3, max_length=60),
    precio: float = Body(ge=1000),
):
    nuevo = {
        "id": id,
        "nombre": nombre,
        "precio": precio,
        "activo": True
    }
    articulos.append(nuevo)
    return nuevo


@app.delete("/articulos/{id}")
async def eliminar_articulo(
    id: int,
    logico: bool = Query(description="Mantener registro?", default=False)
):
    for articulo in articulos:
        if articulo["id"] == id:
            if logico:
                articulo["activo"] = False
            else:
                articulos.remove(articulo)
            return {"mensaje": "Articulo eliminado"}
    return {"mensaje": "Articulo no encontrado"}


@app.put("/articulos/{id}")
async def modificar_articulo(
    id: int = Path(gt=0),
    nombre: str = Body(max_length=50),
    precio: float = Body(ge=1000),
):
    for articulo in articulos:
        if articulo["id"] == id:
            articulo["nombre"] = nombre
            articulo["precio"] = precio
            return articulo

    return {"mensaje": "Articulo no encontrado"}
