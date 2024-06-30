from flask import Flask, request, jsonify
import uuid
from datetime import datetime
import sqlparse
from ollama import chat
from prompts_blueridge import prompt_text_2_sql

app = Flask(__name__)

def generate_query(question):
    # Adapted from your existing code
    updated_prompt = prompt_text_2_sql.format(question=question)
    messages = [
        {
            'role': 'user',
            'content': updated_prompt,
        },
    ]

    response = chat('mannix/defog-llama3-sqlcoder-8b:latest', messages=messages)
    return response['message']['content']

@app.route('/llmInference', methods=['POST'])
def llm_inference():
    # Parse the JSON request payload
    data = request.json
    question = data.get('question', '')

    # Generate unique identifiers for user and session
    user_id = uuid.uuid4()
    session_id = uuid.uuid4()

    # Get the current timestamp in ISO 8601 format
    response_at = datetime.now().isoformat()

    # Generate SQL query
    generated_sql = generate_query(question)

    # Construct the response dictionary
    response = {
        "userId": str(user_id),
        "sessionId": str(session_id),
        "sqlQuery": sqlparse.format(generated_sql, reindent=True),
        "responseAt": response_at
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8002)

