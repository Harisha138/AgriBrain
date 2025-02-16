# AgriBrain 🌾
AgriBrain is an AI-powered chatbot designed to assist farmers with agricultural advice using Google's Gemini API and RAG architecture.

🔧 Setting Up Environment Variables
To ensure your application runs correctly, follow these steps to configure environment variables securely.

1️⃣ Create a .env File

Since the .env file is ignored in Git for security reasons, you need to create one manually:

cp .env.example .env

2️⃣ Add Your Environment Variables

Open the .env file and add your API key:

GOOGLE_API_KEY=your_google_api_key_here
