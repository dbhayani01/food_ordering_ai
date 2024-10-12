import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from meta_ai_api import MetaAI


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes



# Sample menu for pricing
menu = {
    "chicken sandwich": 5.00,
    "fries": 2.00,
    "pizza": 6.00,
    "coke": 1.50,
    "milkshake": 3.00
}

def extract_order_with_model(user_input):
    # Prepare the input for the model
    ai = MetaAI()
    m_input = f"give me json structure without any text in front or after it, from this order details: {user_input} only provide json structure with field visible in input don't add anything else, it should be having name,quantity only in list of dictionaries thats it and menu items are {menu.keys()} so map accordingly"
    response = ai.prompt(message=m_input)
    # print(response['message'])
    return parse_order(response['message'])
 

def parse_order(generated_text):
    # A simple parsing logic to convert model output into order items
    order_details = json.loads(generated_text)
    
    order_details = order_details['order'] if 'order' in order_details else order_details
    order_details = order_details['items'] if 'items' in order_details else order_details
    # This should be replaced with actual parsing logic based on model output
    return order_details if type(order_details) == list else []

@app.route('/order', methods=['POST'])
def order():
    data = request.json
    user_input = data.get("input", "")
    
    # Get order items using the model
    order_items = extract_order_with_model(user_input)
    
    try:
        # Calculate total
        total = 0
        order_items = [order for order in order_items if order['name'].lower() in menu]
        
        total = sum(menu[item['name'].lower()]  * item['quantity'] for item in order_items )
        print(total)
    except KeyError:
        return jsonify({
        "message":"Error in placing the order",
        "order": [],
        "total": 0
    })
    
    # Return response
    return jsonify({
        "message": "Thanks for the order",
        "items": order_items,
        "total": f"${total:.2f}"
    })

if __name__ == '__main__':
    app.run(debug=True)
