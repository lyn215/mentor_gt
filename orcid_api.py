"""
API FastAPI para consultar publicaciones de ORCID
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
from pydantic import BaseModel
from typing import Optional
import re

app = FastAPI(
    title="ORCID Publications API",
    description="API para consultar publicaciones de investigadores desde ORCID",
    version="1.0.0"
)

# Configurar CORS para permitir peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos de respuesta
class Publicacion(BaseModel):
    titulo: str
    tipo: Optional[str] = None
    año: Optional[int] = None
    revista: Optional[str] = None
    doi: Optional[str] = None
    url: Optional[str] = None
    autores: Optional[list[str]] = None

class ORCIDResponse(BaseModel):
    orcid: str
    nombre: Optional[str] = None
    publicaciones: list[Publicacion]
    total: int


def validar_orcid(orcid: str) -> bool:
    """Valida el formato de un ORCID (0000-0000-0000-0000)"""
    patron = r"^\d{4}-\d{4}-\d{4}-\d{3}[\dX]$"
    return bool(re.match(patron, orcid))


async def obtener_nombre_orcid(client: httpx.AsyncClient, orcid: str) -> Optional[str]:
    """Obtiene el nombre del investigador desde ORCID"""
    try:
        response = await client.get(
            f"https://pub.orcid.org/v3.0/{orcid}/person",
            headers={"Accept": "application/json"}
        )
        if response.status_code == 200:
            data = response.json()
            nombre = data.get("name", {})
            given_names = nombre.get("given-names", {}).get("value", "")
            family_name = nombre.get("family-name", {}).get("value", "")
            return f"{given_names} {family_name}".strip() or None
    except Exception:
        pass
    return None


async def obtener_publicaciones_orcid(orcid: str) -> ORCIDResponse:
    """
    Consulta la API pública de ORCID y extrae las publicaciones
    """
    url = f"https://pub.orcid.org/v3.0/{orcid}/works"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Obtener nombre del investigador
        nombre = await obtener_nombre_orcid(client, orcid)
        
        # Obtener publicaciones
        response = await client.get(
            url,
            headers={"Accept": "application/json"}
        )
        
        if response.status_code == 404:
            raise HTTPException(
                status_code=404,
                detail=f"No se encontró el ORCID: {orcid}"
            )
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Error al consultar ORCID: {response.text}"
            )
        
        data = response.json()
        publicaciones = []
        
        # Procesar grupos de trabajos
        grupos = data.get("group", [])
        
        for grupo in grupos:
            work_summaries = grupo.get("work-summary", [])
            if not work_summaries:
                continue
            
            # Tomar el primer resumen del grupo (el más completo)
            work = work_summaries[0]
            
            # Extraer título
            titulo_obj = work.get("title", {})
            titulo = titulo_obj.get("title", {}).get("value", "Sin título")
            
            # Extraer tipo de publicación
            tipo = work.get("type", "").replace("-", " ").title()
            
            # Extraer año
            año = None
            fecha = work.get("publication-date")
            if fecha and fecha.get("year"):
                año = int(fecha["year"]["value"])
            
            # Extraer revista/fuente
            revista = work.get("journal-title", {}).get("value") if work.get("journal-title") else None
            
            # Extraer DOI y URL
            doi = None
            url_pub = None
            external_ids = work.get("external-ids", {}).get("external-id", [])
            for ext_id in external_ids:
                if ext_id.get("external-id-type") == "doi":
                    doi = ext_id.get("external-id-value")
                    url_pub = f"https://doi.org/{doi}"
                    break
            
            if not url_pub:
                url_pub = work.get("url", {}).get("value") if work.get("url") else None
            
            publicacion = Publicacion(
                titulo=titulo,
                tipo=tipo or None,
                año=año,
                revista=revista,
                doi=doi,
                url=url_pub
            )
            publicaciones.append(publicacion)
        
        # Ordenar por año (más recientes primero)
        publicaciones.sort(key=lambda x: x.año or 0, reverse=True)
        
        return ORCIDResponse(
            orcid=orcid,
            nombre=nombre,
            publicaciones=publicaciones,
            total=len(publicaciones)
        )


@app.get("/")
async def root():
    """Endpoint raíz con información de la API"""
    return {
        "mensaje": "API de consulta de publicaciones ORCID",
        "documentacion": "/docs",
        "uso": "GET /publicaciones/{orcid}"
    }


@app.get("/publicaciones/{orcid}", response_model=ORCIDResponse)
async def get_publicaciones(orcid: str):
    """
    Obtiene las publicaciones de un investigador desde ORCID.
    
    - **orcid**: Identificador ORCID del investigador (formato: 0000-0000-0000-0000)
    
    Retorna la lista de publicaciones con título, tipo, año, revista, DOI y URL.
    """
    # Validar formato del ORCID
    if not validar_orcid(orcid):
        raise HTTPException(
            status_code=400,
            detail="Formato de ORCID inválido. Use el formato: 0000-0000-0000-0000"
        )
    
    return await obtener_publicaciones_orcid(orcid)


@app.get("/health")
async def health_check():
    """Endpoint de salud para verificar que la API está funcionando"""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

