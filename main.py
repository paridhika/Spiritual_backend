from openai import OpenAI

client = OpenAI(api_key="YOUR_TOKEN")

models = client.models.list()

for model in models.data:
    print(model.id)
# vedic_chat.py
from openai import OpenAI

# 1️⃣ Initialize OpenAI client
client = OpenAI(api_key="YOUR_TOKEN")

# 2️⃣ Vedic scholar system prompt
SYSTEM_PROMPT = """
You are an expert scholar in Hindu scriptures, including the Vedas, Upanishads, Bhagavad Gita, and Puranas.
Provide accurate, clear, and contextual explanations.

Guidelines:
1. Structure the answer clearly with sections or bullet points.
2. Include scriptural or philosophical references (e.g., Bhagavad Gita 2.47, Rig Veda 10.90).
3. Define Sanskrit terms precisely (e.g., Dharma, Atman, Karma).
4. Add philosophical, moral, or spiritual interpretations where relevant.
5. Maintain a tone that is scholarly yet accessible.

User Query: {user_query}

Assistant Response:
"""
# 3️⃣ Conversation history
conversation = [{"role": "system", "content": SYSTEM_PROMPT}]

# 4️⃣ Query function
def query_veda(user_input: str, preferred_model="gpt-4o", max_tokens=700):
    conversation.append({"role": "user", "content": user_input})
    models_to_try = [preferred_model, "gpt-4o-mini", "gpt-3.5-turbo"]

    for model in models_to_try:
        try:
            print(f"\n🔹 Using model: {model}")
            response = client.chat.completions.create(
                model=model,
                messages=conversation,
                temperature=0.7,
                max_tokens=max_tokens,
                top_p=0.9,
            )
            reply = response.choices[0].message.content
            # Add assistant reply to conversation
            conversation.append({"role": "assistant", "content": reply})
            return reply
        except Exception as e:
            print(f"⚠️ Failed with {model}: {e}")
            continue

    return "❌ All available models failed. Please check your API key or network connection."

# 5️⃣ Interactive console
if __name__ == "__main__":
    print("🕉️  Vedic ChatGPT Interface (context-aware) (type 'exit' to quit)")
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if user_input.lower() in ["exit", "quit"]:
                print("🙏 Exiting. May wisdom guide your path.")
                break
            if not user_input:
                continue
            reply = query_veda(user_input)
            print("\nAssistant:", reply)
        except KeyboardInterrupt:
            print("\n🙏 Exiting gracefully.")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

     
