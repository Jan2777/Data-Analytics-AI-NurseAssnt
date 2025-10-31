from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app, resources={r"/*": {"origins": ["http://127.0.0.1:5500", "http://localhost:5500"]}})

def process_with_llm(input_text, task):
    if task == "summarize":
        prompt = f"Summarize this Tamil patient note in English: {input_text}"
    elif task == "translate":
        prompt = f"Translate this Tamil text to English: {input_text}"
    elif task == "symptom_analysis":
        prompt = f"Analyze these symptoms in Tamil and give basic advice in English: {input_text}"
    elif task == "medication_reminder":
        prompt = f"Set a reminder for this medication in Tamil: {input_text}. Respond in English with a simple schedule."
    elif task == "cultural_tip":
        prompt = f"Provide a Tamil cultural health tip (e.g., Ayurvedic) for this issue in English: {input_text}"
    else:
        prompt = input_text

    completion = client.chat.completions.create(
        model="gpt-4o-mini",  # ✅ new models (use gpt-4o or gpt-4o-mini)
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )

    return completion.choices[0].message.content.strip()

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/process', methods=['POST'])
def process_input():
    try:
        data = request.get_json()
        input_text = data.get('text', '')
        task = data.get('task', 'summarize')

        if not input_text:
            return jsonify({'error': 'No input text provided'}), 400

        result = process_with_llm(input_text, task)
        return jsonify({'output': result})

    except Exception as e:
        print("Error:", e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
