# AI Food Ordering System

## Overview

This project is an AI-driven food ordering system that allows users to place orders via a chat interface. Built using Flask for the backend and React for the frontend, this system leverages a Generative AI model to extract order details from user input and calculate the total cost based on a predefined menu.

## Features

- Chat interface for seamless user interaction.
- Ability to place orders with multiple items.
- Intelligent extraction of order details using a Generative AI model.
- CORS enabled for cross-origin requests.
- Responsive design suitable for various devices.

## Technologies Used

- **Frontend:** React
- **Backend:** Flask
- **AI Model:** GPT-2 (or another suitable generative AI model)
- **Dependencies:**
  - Flask
  - Flask-CORS
  - Transformers (for the AI model)
  - PyTorch (for running the AI model)

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- Node.js (for React)

### Installation

1. **Clone the Repository:**

   ```bash
   git clone <repository-url>
   cd <repository-folder>
   
2. **Set Up the Python Virtual Environment:**

    python -m venv fo_ai
    cd fo_ai
    .\Scripts\activate  # Activate the virtual environment on Windows

3. **Install Python Dependencies:**
    
    pip install -r requirements.txt

4. **Set Up the React Frontend:**
   
   Navigate to the React app folder (if it's separate) and run:
    
    - npm install


