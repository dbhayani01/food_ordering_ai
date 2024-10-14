import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from meta_ai_api import MetaAI

app = Flask(__name__)
CORS(app)

# Sample menu for pricing
menu = {
    "chicken sandwich": 5.00,
    "fries": 2.00,
    "pizza": 6.00,
    "coke": 1.50,
    "milkshake": 3.00
}

def extract_order_with_model(user_input):
    ai = MetaAI()
    m_input = f"Extract order details from the following input: '{user_input}'. Provide a JSON structure without any text in front or after it containing a list of dictionaries with the fields 'name' and 'quantity' based on the menu: {menu.keys()}, if you are able to extract order details just share the JSON just a list of order items ,as i can directly process it."
    response = ai.prompt(message=m_input)
    print(response['message'])
    return parse_order(response['message'])

def parse_order(generated_text):
    try:
        order_details = json.loads(generated_text)
        # order_details = order_details.get('order', order_details)
        # order_details = order_details.get('items', order_details)
        return order_details if isinstance(order_details, list) else []
    except json.JSONDecodeError:
        return []  # Return an empty list if parsing fails

@app.route('/conversation', methods=['POST'])
def conversation():
    data = request.json
    user_input = data.get("input", "").strip()

    # Send user input to the AI for processing
    ai = MetaAI()
    # response = ai.prompt(message=f"Respond to the following input as food ordering bot and stay in content to taking food orders and decline other questions politely and if they ask for a menu here it is {menu}: '{user_input}'. Include any order details if applicable.")
    # Enhanced prompt for the AI to behave as a food ordering bot
    prompt_message = (
        "You are a food ordering bot. Your primary function is to assist users in placing food orders. "
        "Please only focus on food-related questions and politely decline any unrelated inquiries. "
        "If the user asks for the menu, respond with the following items: " + ', '.join(menu.keys()) + ". "
        "You should remember the user's order until they confirm it. "
        "Once confirmend and placed just share him the total no payment or checkout needs to be done"
        "User input: '{}'"
    ).format(user_input)
    response = ai.prompt(message=prompt_message)
    if response['message']:  # Check if there's a generated response
        order_items = extract_order_with_model(user_input)

        if order_items:  # If valid order details were extracted
            total = sum(menu[item['name'].lower()] * item['quantity'] for item in order_items if item['name'].lower() in menu)
            order_confirmation_message = f"{response['message']} Thanks for your order! Your total is ${total:.2f}."
            return jsonify({
                "message": order_confirmation_message,
                "items": order_items,
                "total": f"${total:.2f}"
            })
        
        # If no order details, just return the AI's response
        return jsonify({
            "message": response['message']
        })
    
    # Default response if AI fails to generate a valid response
    return jsonify({
        "message": "I'm not able to process that right now. Please try asking about the menu or placing an order."
    })

if __name__ == '__main__':
    app.run(debug=True)
