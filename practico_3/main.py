from typing import Annotated

from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field

app = FastAPI()

app.title = "API de articulos de futbol"


NOT_FOUND_RESPONSE = {
    404: {
        "description": "Articulo no encontrado",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Articulo no encontrado"
                }
            }
        },
    },
}



IntPositivo = Annotated[int, Field(gt=0)]
StrNombreArticulo = Annotated[str, Field(min_length=3, max_length=40)]
PrecioArticulo = Annotated[int, Field(gt=1000, lt=999999)]
BoolActivo = Annotated[bool, Field(description="Articulo disponible")]



class ArticuloSchema(BaseModel):
    id: IntPositivo
    nombre: StrNombreArticulo
    precio: PrecioArticulo
    activo: BoolActivo = True


class ArticuloUpdateSchema(BaseModel):
    nombre: StrNombreArticulo
    precio: PrecioArticulo
    activo: BoolActivo = True



articulos = [
    {"id": 1, "nombre": "Pelota Adidas", "precio": 15000, "activo": True},
    {"id": 2, "nombre": "Botines Nike", "precio": 45000, "activo": True},
    {"id": 3, "nombre": "Camiseta Argentina", "precio": 30000, "activo": True},
]



@app.get("/articulos", response_model=list[ArticuloSchema])
async def ver_articulos():
    return articulos



@app.get(
    "/articulos/{id}",
    responses=NOT_FOUND_RESPONSE,
    response_model=ArticuloSchema,
)
async def ver_articulo_por_id(
    id: Annotated[int, Path(gt=0)]
):
    for articulo in articulos:
        if articulo["id"] == id:
            return articulo

    raise HTTPException(
        status_code=404,
        detail="Articulo no encontrado"
    )



@app.post(
    "/articulos",
    response_model=list[ArticuloSchema]
)
async def agregar_articulo(
    articulo_nuevo: ArticuloSchema
):
    articulos.append(articulo_nuevo.model_dump())
    return articulos


@app.delete(
    "/articulos/{id}",
    responses=NOT_FOUND_RESPONSE,
    response_model=ArticuloSchema,
)
async def eliminar_articulo(
    id: Annotated[int, Path(gt=0)],
    logico: Annotated[
        bool,
        Query(description="Mantener registro?")
    ] = False,
):

    for articulo in articulos:
        if articulo["id"] == id:

            if logico:
                articulo["activo"] = False
            else:
                articulos.remove(articulo)

            return articulo

    raise HTTPException(
        status_code=404,
        detail="Articulo no encontrado"
    )



@app.put(
    "/articulos/{id}",
    responses=NOT_FOUND_RESPONSE,
    response_model=ArticuloSchema,
)
async def modificar_articulo(
    id: Annotated[int, Path(gt=0)],
    articulo_editado: ArticuloUpdateSchema,
):

    for articulo in articulos:
        if articulo["id"] == id:

            articulo["nombre"] = articulo_editado.nombre
            articulo["precio"] = articulo_editado.precio
            articulo["activo"] = articulo_editado.activo

            return articulo

    raise HTTPException(
        status_code=404,
        detail="Articulo no encontrado"
    )