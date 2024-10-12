import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import GPT2LMHeadModel, GPT2Tokenizer

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load GPT-2 Model and Tokenizer
model_name = 'gpt2'  # or 'gpt2-medium', 'gpt2-large', etc.
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Sample menu for pricing
menu = {
    "chicken sandwich": 5.00,
    "fries": 2.00,
    "cheeseburger": 6.00,
    "coke": 1.50,
    "milkshake": 3.00
}

def extract_order_with_model(user_input):
    # Prepare the input for the model
    input_text = f"Extract the order from the following input: '{user_input}'"
    input_ids = tokenizer.encode(input_text, return_tensors='pt')
    
    # Generate response from the model
    output = model.generate(input_ids, max_length=50, num_return_sequences=1)
    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    
    # Here, we would implement a parsing function to extract the order from generated_text
    # For simplicity, we'll just simulate this
    return parse_order(generated_text)

def parse_order(generated_text):
    # A simple parsing logic to convert model output into order items
    order_items = []
    
    # This should be replaced with actual parsing logic based on model output
    for item_name in menu.keys():
        if item_name in generated_text:
            order_items.append({"name": item_name, "quantity": 1})  # You might want to adjust quantities based on input
    
    return order_items

@app.route('/order', methods=['POST'])
def order():
    data = request.json
    user_input = data.get("input", "")
    
    # Get order items using the model
    order_items = extract_order_with_model(user_input)
    
    # Calculate total
    total = sum(menu[item['name']] * item['quantity'] for item in order_items)
    
    # Return response
    return jsonify({
        "order": order_items,
        "total": f"${total:.2f}"
    })

if __name__ == '__main__':
    app.run(debug=True)
