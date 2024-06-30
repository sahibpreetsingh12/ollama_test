from flask import Flask, request, jsonify,Blueprint
import uuid
from datetime import datetime
import sqlparse
import requests
import json
from ollama import chat
from prompts_blueridge import prompt_text_2_sql

app = Flask(__name__)



# Create a blueprint for the main routes
# main = Blueprint('main', __name__)


def generate_query(question, model="mannix/defog-llama3-sqlcoder-8b:latest"):
    updated_prompt = prompt_text_2_sql.format(question=question)
    url = "http://localhost:11434/api/chat"
    data = {
        "model": model,
        "messages": [{"role": "user", "content": updated_prompt}],
        "stream": True
    }
    
    full_response = ""
    with requests.post(url, json=data, stream=True) as response:
        for line in response.iter_lines():
            if line:
                json_response = json.loads(line)
                if 'message' in json_response and 'content' in json_response['message']:
                    full_response += json_response['message']['content']
    
    return full_response.strip()

# def generate_query(question):
#     # Adapted from your existing code
#     updated_prompt = prompt_text_2_sql.format(question=question)
#     messages = [
#         {
#             'role': 'user',
#             'content': updated_prompt,
#         },
#     ]

#     response = chat('mannix/defog-llama3-sqlcoder-8b:latest', messages=messages)
#     return response['message']['content']

@app.route('/llmInference', methods=['POST'])
def llm_inference():
    """
    Handle POST requests to generate SQL query based on user question.

    This endpoint accepts a JSON payload with a 'question' field, generates
    a SQL query using the pre-trained model, and returns a JSON response
    containing the user ID, session ID, generated SQL query, and the response timestamp.

    Returns:
        JSON: A JSON response with userId, sessionId, sqlQuery, and responseAt fields.

    
    """
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
    app.run(host='0.0.0.0', port=8080)