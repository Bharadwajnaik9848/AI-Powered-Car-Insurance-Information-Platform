import os
import uuid
from datetime import datetime, timedelta

from flask import Blueprint, current_app, jsonify, render_template, request
from flask_login import current_user, login_required

from config.database import db
from models.chat import ChatMessage, ChatSession
from utils.mistral_ai import get_ai_response

chat = Blueprint('chat', __name__)

@chat.route('/chat')
@login_required
def chat_interface():
    session_id = request.args.get('session_id')
    if not session_id:
        session = ChatSession(
            session_id=str(uuid.uuid4()),
            user_id=current_user.id
        )
        db.session.add(session)
        db.session.commit()
        session_id = session.session_id
    
    chat_session = ChatSession.query.filter_by(
        session_id=session_id,
        user_id=current_user.id
    ).first_or_404()
    
    messages = ChatMessage.query.filter_by(session_id=chat_session.id).order_by(ChatMessage.timestamp).all()
    
    return render_template('chat/interface.html', 
                         session_id=session_id,
                         messages=messages)

@chat.route('/chat/send', methods=['POST'])
@login_required
def send_message():
    data = request.json
    session_id = data.get('session_id')
    content = data.get('message')
    
    if not session_id or not content:
        return jsonify({'error': 'Missing session_id or message'}), 400
    
    # Check rate limiting
    recent_messages = ChatMessage.query.filter(
        ChatMessage.session_id == ChatSession.query.filter_by(session_id=session_id).first().id,
        ChatMessage.timestamp >= datetime.utcnow() - timedelta(minutes=1)
    ).count()
    
    if recent_messages >= 10:  # Max 10 messages per minute
        return jsonify({'error': 'Rate limit exceeded. Please wait a moment.'}), 429
    
    chat_session = ChatSession.query.filter_by(
        session_id=session_id,
        user_id=current_user.id
    ).first_or_404()
    
    # Save user message
    user_message = ChatMessage(
        session_id=chat_session.id,
        role='user',
        content=content
    )
    db.session.add(user_message)
    
    # Get chat history (last 10 messages for context)
    history = ChatMessage.query.filter_by(session_id=chat_session.id)\
        .order_by(ChatMessage.timestamp.desc())\
        .limit(10)\
        .all()
    history.reverse()
    
    messages = [{"role": msg.role, "content": msg.content} for msg in history]
    messages.append({"role": "user", "content": content})
    
    try:
        # Get AI response
        ai_content = get_ai_response(messages)
        
        # Save AI response
        ai_message = ChatMessage(
            session_id=chat_session.id,
            role='assistant',
            content=ai_content
        )
        db.session.add(ai_message)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': ai_content
        })
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Chat error: {str(e)}")
        return jsonify({'error': 'An error occurred while processing your request.'}), 500

@chat.route('/chat/history')
@login_required
def get_history():
    session_id = request.args.get('session_id')
    if not session_id:
        return jsonify({'error': 'Missing session_id'}), 400
    
    chat_session = ChatSession.query.filter_by(
        session_id=session_id,
        user_id=current_user.id
    ).first_or_404()
    
    messages = ChatMessage.query.filter_by(session_id=chat_session.id)\
        .order_by(ChatMessage.timestamp)\
        .all()
    
    return jsonify({
        'messages': [msg.to_dict() for msg in messages]
    })
