import os
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
conversations = {}

@app.route('/')
def home():
    return jsonify({
        "message": "🕉️ Spiritual & Emotional Therapy API",
        "version": "1.0",
        "endpoints": {
            "/chat": "POST - Send a message",
            "/reset": "POST - Reset conversation"
        }
    })

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_input = data.get('message', '').strip()
        session_id = data.get('session_id', 'default')
        model = data.get('model', 'gpt-4o')
        max_tokens = data.get('max_tokens', 800)
        
        if not user_input:
            return jsonify({"error": "Message cannot be empty"}), 400
        
        # Initialize conversation for new sessions
        if session_id not in conversations:
            conversations[session_id] = [
                {"role": "system", "content": SYSTEM_PROMPT}
            ]
        
        # Add user message to conversation
        conversations[session_id].append({"role": "user", "content": user_input})
        
        # Try models in order of preference
        models_to_try = [model, "gpt-4o-mini", "gpt-3.5-turbo"]
        
        for current_model in models_to_try:
            try:
                response = client.chat.completions.create(
                    model=current_model,
                    messages=conversations[session_id],
                    temperature=0.7,
                    max_tokens=max_tokens,
                    top_p=0.9,
                )
                
                reply = response.choices[0].message.content
                
                # Add assistant reply to conversation
                conversations[session_id].append({"role": "assistant", "content": reply})
                
                return jsonify({
                    "response": reply,
                    "model_used": current_model,
                    "session_id": session_id,
                    "conversation_length": len(conversations[session_id])
                })
                
            except Exception as e:
                print(f"⚠️ Failed with {current_model}: {e}")
                continue
        
        return jsonify({"error": "All available models failed"}), 500
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/reset', methods=['POST'])
def reset_conversation():
    try:
        data = request.json
        session_id = data.get('session_id', 'default')
        
        if session_id in conversations:
            conversations[session_id] = [
                {"role": "system", "content": SYSTEM_PROMPT}
            ]
            return jsonify({"message": "Conversation reset successfully", "session_id": session_id})
        else:
            return jsonify({"message": "No active conversation found", "session_id": session_id})
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
