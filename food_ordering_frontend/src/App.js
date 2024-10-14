import React, { useState } from 'react';
import './App.css';

function App() {
  const [order, setOrder] = useState('');
  const [messages, setMessages] = useState([{"sender":"bot","text":"Hi! What do you want to order today?"}]);
  const [errorMessage, setErrorMessage] = useState('');
  const [retryOrder, setRetryOrder] = useState(null);

  const handleInputChange = (e) => {
    setOrder(e.target.value);
  };

  const handleSendOrder = async (retry = false) => {
    let currentOrder = retry ? retryOrder : order;

    if (currentOrder.trim() === '') {
      alert('Please type an order!');
      return;
    }

    if (!retry) {
      setMessages((prevMessages) => [
        ...prevMessages,
        { sender: 'user', text: currentOrder }
      ]);
    }

    try {
      const res = await fetch('http://127.0.0.1:5000/conversation', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ input: currentOrder }),
      });

      const data = await res.json();
      
      if (res.ok) {
        setMessages((prevMessages) => [
          ...prevMessages,
          { sender: 'bot', text: data.message }
        ]);
        setErrorMessage('');
        setRetryOrder(null);
      } else {
        throw new Error('Server error');
      }
    } catch (error) {
      console.error('Error:', error);
      handleErrorMessage(currentOrder);
    }

    setOrder('');
  };

  const handleErrorMessage = (currentOrder) => {
    const errorText = `Order failed! Please try again.`;
    setErrorMessage(errorText);
    setRetryOrder(currentOrder);

    setMessages((prevMessages) => [
      ...prevMessages,
      { sender: 'error', text: errorText }
    ]);
  };

  return (
    <div className="app-container">
      <div className="chatbot-section">
        <div className="chatbox">
          <div className="chat-header">
            <h3>Order Food with AI</h3>
          </div>
          <div className="chat-body">
            {messages.map((message, index) => (
              <div
                key={index}
                className={`message ${
                  message.sender === 'user'
                    ? 'user-message'
                    : message.sender === 'bot'
                    ? 'bot-message'
                    : 'error-message'
                }`}
              >
                {message.sender === 'error' && (
                  <span className="error-icon">❗</span>
                )}
                {message.text}
                {message.sender === 'error' && (
                  <button className="retry-button" onClick={() => handleSendOrder(true)}>
                    Reorder
                  </button>
                )}
              </div>
            ))}
          </div>
          <div className="chat-input">
            <input
              type="text"
              value={order}
              onChange={handleInputChange}
              placeholder="Type your order..."
            />
            <button onClick={() => handleSendOrder(false)}>Send</button>
          </div>
        </div>
      </div>
      <div className="info-section">
        <h1>AI Takes Your Food Order in Seconds</h1>
        <p>
          Experience quick and seamless food ordering with our AI-driven system.
          Place your order now!
        </p>
        <div className="image-container">
          <img src="/pizza.jpeg" alt="Pizza" className="food-image" />
          <img src="/milkshake.jpeg" alt="Milkshake" className="food-image" />
          <img src="/sandwich.jpeg" alt="Sandwich" className="food-image" />
          <img src="/coke_can.jpeg" alt="Coke" className="food-image" />
        </div>
      </div>
    </div>
  );
}

export default App;
