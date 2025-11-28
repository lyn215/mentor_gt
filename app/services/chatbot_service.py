from groq import Groq
from flask import current_app
from app.models.usuario import Usuario
from app.models.publicacion import Publicacion
from app.models.evento import Evento
from app.models.docencia import Docencia
from datetime import datetime

class ChatbotService:
    """Chatbot con IA usando Groq (Llama 3.3)"""
    
    def __init__(self):
        api_key = current_app.config.get('GROQ_API_KEY')
        if not api_key:
            raise ValueError("GROQ_API_KEY no configurada")
        self.client = Groq(api_key=api_key)
    
    def generar_respuesta(self, pregunta: str, usuario_id: int, historial: list = None) -> dict:
        """
        Genera respuesta usando Groq (Llama 3.3)
        
        Args:
            pregunta: Pregunta del usuario
            usuario_id: ID del usuario
            historial: Lista de mensajes previos (opcional)
        
        Returns:
            dict con 'respuesta' y 'metadata'
        """
        
        # Obtener datos del usuario
        usuario = Usuario.query.get(usuario_id)
        publicaciones = Publicacion.query.filter_by(usuario_id=usuario_id).all()
        eventos = Evento.query.filter_by(usuario_id=usuario_id).all()
        docencias = Docencia.query.filter_by(usuario_id=usuario_id).all()
        
        # Construir contexto del CV
        contexto = self._construir_contexto_cv(usuario, publicaciones, eventos, docencias)
        
        # Construir el sistema prompt
        system_prompt = f"""Eres un asistente académico especializado en ayudar a profesores universitarios con sus CVs.

INFORMACIÓN DEL PROFESOR:
{contexto}

INSTRUCCIONES:
- Responde de manera clara, profesional y útil
- Si te preguntan sobre datos del CV, usa la información proporcionada
- Si te piden generar un CV, explica los pasos para hacerlo
- Si te piden sincronizar, explica cómo configurar ORCID
- Sé conciso pero informativo
- Usa emojis ocasionalmente para hacer la conversación más amigable
- Si no tienes información, sugiere al usuario agregarla al sistema"""

        # Preparar mensajes para la API
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        # Agregar historial si existe
        if historial:
            messages.extend(historial)
        
        # Agregar pregunta actual
        messages.append({
            "role": "user",
            "content": pregunta
        })
        
        try:
            # Llamar a Groq API
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model="llama-3.3-70b-versatile",  # Modelo más potente de Groq
                temperature=0.7,  # Balance entre creatividad y coherencia
                max_tokens=1024,
                top_p=1,
                stream=False
            )
            
            respuesta = chat_completion.choices[0].message.content
            
            # Detectar si el usuario quiere generar CV
            es_solicitud_cv = self._detectar_intencion_generar_cv(pregunta)
            
            return {
                'respuesta': respuesta,
                'metadata': {
                    'timestamp': datetime.now().isoformat(),
                    'modelo': 'llama-3.3-70b',
                    'tokens_usados': chat_completion.usage.total_tokens,
                    'es_solicitud_cv': es_solicitud_cv
                }
            }
            
        except Exception as e:
            return {
                'respuesta': f"Lo siento, hubo un error al procesar tu pregunta: {str(e)}",
                'metadata': {
                    'timestamp': datetime.now().isoformat(),
                    'error': True
                }
            }
    
    def _construir_contexto_cv(self, usuario, publicaciones, eventos, docencias):
        """Construye el contexto del CV para el chatbot"""
        
        contexto = f"""
DATOS PERSONALES:
- Nombre: {usuario.nombre} {usuario.apellidos or ''}
- Email: {usuario.email}
- ORCID ID: {usuario.orcid_id or 'No configurado'}
- Scopus ID: {usuario.scopus_id or 'No configurado'}
- Google Scholar ID: {usuario.google_scholar_id or 'No configurado'}

PUBLICACIONES ({len(publicaciones)} total):
"""
        
        if publicaciones:
            # Ordenar por año descendente
            pubs_ordenadas = sorted(publicaciones, key=lambda x: x.año or 0, reverse=True)
            
            # Mostrar las 10 más recientes
            for pub in pubs_ordenadas[:10]:
                contexto += f"- [{pub.año or 'N/A'}] {pub.titulo}\n"
                if pub.revista:
                    contexto += f"  Revista: {pub.revista}\n"
                if pub.doi:
                    contexto += f"  DOI: {pub.doi}\n"
            
            if len(publicaciones) > 10:
                contexto += f"\n... y {len(publicaciones) - 10} publicaciones más\n"
            
            # Estadísticas por año
            por_año = {}
            for pub in publicaciones:
                año = pub.año or "Sin año"
                por_año[año] = por_año.get(año, 0) + 1
            
            contexto += f"\nDistribución por año:\n"
            for año, cant in sorted(por_año.items(), reverse=True):
                contexto += f"- {año}: {cant} publicación{'es' if cant != 1 else ''}\n"
        else:
            contexto += "No hay publicaciones registradas aún.\n"
        
        contexto += f"\nEVENTOS ACADÉMICOS ({len(eventos)} total):\n"
        if eventos:
            for evento in eventos[:5]:
                fecha = evento.fecha_inicio.strftime('%Y-%m-%d') if evento.fecha_inicio else 'N/A'
                contexto += f"- {evento.nombre} ({fecha}) - Rol: {evento.rol or 'N/A'}\n"
            
            if len(eventos) > 5:
                contexto += f"... y {len(eventos) - 5} eventos más\n"
        else:
            contexto += "No hay eventos registrados aún.\n"
        
        contexto += f"\nEXPERIENCIA DOCENTE ({len(docencias)} total):\n"
        if docencias:
            for doc in docencias[:5]:
                contexto += f"- {doc.nombre_curso} ({doc.año or 'N/A'}) - {doc.nivel or 'N/A'}\n"
            
            if len(docencias) > 5:
                contexto += f"... y {len(docencias) - 5} cursos más\n"
        else:
            contexto += "No hay experiencia docente registrada aún.\n"
        
        return contexto
    
    def _detectar_intencion_generar_cv(self, pregunta: str) -> bool:
        """Detecta si el usuario quiere generar un CV"""
        palabras_clave = ['genera', 'generar', 'crear', 'crea', 'cv', 'curriculum', 
                          'reporte', 'documento', 'pdf', 'word', 'descargar']
        pregunta_lower = pregunta.lower()
        return any(palabra in pregunta_lower for palabra in palabras_clave)
    
    def generar_respuesta_streaming(self, pregunta: str, usuario_id: int):
        """
        Genera respuesta en modo streaming (para efecto de "escribiendo")
        """
        usuario = Usuario.query.get(usuario_id)
        publicaciones = Publicacion.query.filter_by(usuario_id=usuario_id).all()
        eventos = Evento.query.filter_by(usuario_id=usuario_id).all()
        docencias = Docencia.query.filter_by(usuario_id=usuario_id).all()
        
        contexto = self._construir_contexto_cv(usuario, publicaciones, eventos, docencias)
        
        system_prompt = f"""Eres un asistente académico especializado.

INFORMACIÓN DEL PROFESOR:
{contexto}

Responde de manera clara y profesional."""

        try:
            stream = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": pregunta}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.7,
                max_tokens=1024,
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            yield f"Error: {str(e)}"