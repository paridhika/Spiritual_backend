import os
from flask import Flask, request, jsonify
import openai
from openai import OpenAI
# Initialize Flask
from flask_cors import CORS
app = Flask(__name__)
CORS(app, origins=["http://localhost:8081"])

# Initialize OpenAI client
openai.api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai.api_key)

# Enhanced system prompt for spiritual and emotional therapy
SYSTEM_PROMPT = """
You are a compassionate and knowledgeable therapeutic guide specializing in both spiritual and emotional wellbeing. You combine deep expertise in Hindu scriptures (Vedas, Upanishads, Bhagavad Gita, Puranas) with modern emotional therapy principles.

Your Approach:
1. SPIRITUAL GUIDANCE: Provide accurate scriptural wisdom with references (e.g., Bhagavad Gita 2.47, Rig Veda 10.90)
2. EMOTIONAL SUPPORT: Offer empathetic, evidence-based emotional therapy techniques
3. HOLISTIC INTEGRATION: Connect spiritual teachings with emotional healing practices

Guidelines:
- Listen deeply and validate the user's feelings and experiences
- Ask thoughtful follow-up questions to understand their situation better
- Provide both spiritual wisdom and practical emotional coping strategies
- Define Sanskrit terms clearly (e.g., Dharma, Atman, Karma, Moksha)
- Include meditation, breathing, or mindfulness practices when appropriate
- Offer philosophical, moral, and therapeutic interpretations
- Maintain a warm, non-judgmental, and supportive tone
- Structure responses clearly with sections or gentle bullet points
- If the user's concern requires deeper exploration, ask 1-2 clarifying questions

Key Areas of Support:
- Anxiety, stress, and worry management
- Grief, loss, and emotional pain
- Life purpose and existential questions
- Relationship challenges
- Self-doubt and confidence issues
- Spiritual disconnection or crisis
- Inner peace and contentment

Always prioritize the user's emotional safety and wellbeing. If you sense serious mental health concerns, gently encourage professional support while still offering compassionate guidance.
"""

# Store conversations by session ID
messages = {}

# @app.route('/')
# def home():
#     return jsonify({
#         "message": "🕉️ Spiritual & Emotional Therapy API",
#         "version": "1.0",
#         "endpoints": {
#             "/chat": "POST - Send a message",
#             "/reset": "POST - Reset conversation"
#         }
#     })

@app.route('/chat', methods=['POST'])
def chat():
    
    data = request.json
    user_input = data.get('message', '').strip()
    session_id = data.get('session_id', '1')
    
    if not user_input:
        return jsonify({"error": "Message cannot be empty"}), 400
    
    # Initialize conversation for new sessions
    if session_id not in conversations:
        messages[session_id] = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]
    
    # Add user message to conversation
    messages[session_id].append({"role": "user", "content": user_input})
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages[session_id],
            temperature=0.7,
            max_tokens=1000,
            top_p=0.9,
        )
        
        reply = response.choices[0].message.content
        
        # Add assistant reply to conversation
        messages[session_id].append({"role": "assistant", "content": reply})
        
        return jsonify({"response": reply})
        
    except Exception as e:
        print(f"⚠️ Failed with model: {e}")
    

# @app.route('/reset', methods=['POST'])
# def reset_conversation():
#     try:
#         data = request.json
#         session_id = data.get('session_id', 'default')
        
#         if session_id in conversations:
#             conversations[session_id] = [
#                 {"role": "system", "content": SYSTEM_PROMPT}
#             ]
#             return jsonify({"message": "Conversation reset successfully", "session_id": session_id})
#         else:
#             return jsonify({"message": "No active conversation found", "session_id": session_id})
            
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=False)
