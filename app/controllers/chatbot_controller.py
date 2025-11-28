from flask import Blueprint, render_template, request, jsonify, Response, stream_with_context
from flask_login import login_required, current_user
from app import csrf  # ⬅️ AGREGAR ESTA LÍNEA
from app.services.chatbot_service import ChatbotService
from app.utils.decorators import profesor_required
from datetime import datetime
import json

chatbot_bp = Blueprint('chatbot', __name__)

@chatbot_bp.route('/')
@login_required
@profesor_required
def index():
    """Página del chatbot"""
    return render_template('profesor/chatbot.html')

@chatbot_bp.route('/mensaje', methods=['POST'])
@login_required
@profesor_required
@csrf.exempt  # ⬅️ AGREGAR ESTA LÍNEA
def enviar_mensaje():
    data = request.get_json()
    pregunta = data.get('mensaje', '')
    
    print(f"📩 Datos recibidos: {data}")
    print(f"📩 Mensaje: {pregunta}")
    
    if not pregunta:
        print("❌ Mensaje vacío")
        return jsonify({'error': 'Mensaje vacío'}), 400
    
    try:
        print("🤖 Creando ChatbotService...")
        chatbot_service = ChatbotService()
        print("✅ ChatbotService creado")
        
        resultado = chatbot_service.generar_respuesta(pregunta, current_user.id)
        print(f"✅ Respuesta generada")
        
        return jsonify(resultado)
        
    except Exception as e:
        print(f"❌ ERROR COMPLETO: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return jsonify({
            'respuesta': f'Lo siento, hubo un error: {str(e)}',
            'metadata': {'timestamp': datetime.now().isoformat(), 'error': True}
        }), 500
@chatbot_bp.route('/stream', methods=['POST'])
@login_required
@profesor_required
def stream_mensaje():
    """API para recibir respuesta en streaming (efecto de escritura)"""
    data = request.get_json()
    pregunta = data.get('mensaje', '')
     
    print(f"📩 Datos recibidos: {data}")  # ⬅️ ¿Está esto?
    print(f"📩 Mensaje: {pregunta}")      # ⬅️ ¿Está esto?
    if not pregunta:
        return jsonify({'error': 'Mensaje vacío'}), 400
    
    def generate():
        chatbot_service = ChatbotService()
        for chunk in chatbot_service.generar_respuesta_streaming(pregunta, current_user.id):
            yield f"data: {json.dumps({'chunk': chunk})}\n\n"
    
    return Response(stream_with_context(generate()), mimetype='text/event-stream')