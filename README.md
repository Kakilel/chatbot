Fred – AI Chatbot
Fred is a smart, modular AI chatbot built with Python and PyQt6. It combines the power of the Gemini Flash API with specialized APIs for movies, math, trivia, time, meals, and more. Fred can answer questions, solve math problems, show movies, plan meals, and even teach you history using Wikipedia.

 Features
 Conversational AI (Gemini Flash API)

 Movie Search & Recommendations (TMDB API)

 Math Solving, Graphs, Stats & Step-by-Step (SymPy, WolframAlpha)

 Time & Location Inference (WorldTime API)

 Weather Forecasts (Weather API)

 Meal Planning (MealDB API)

 Fallback Knowledge Mode (Wikipedia Summary)

 Modular API routing with natural language triggers

 PyQt6 GUI interface with dynamic response rendering

 Getting Started


1. Clone the repository
Copy
git clone https://github.com/yourusername/fred-chatbot.git
cd fred-chatbot


2. Install dependencies

pip install -r requirements.txt


3. Set up environment variables
Create a .env file in the root directory:




4. Run the chatbot
bash
Copy
Edit
python chatbot.py



Example Commands
"Who directed Inception?" → Movie info via TMDB

"Differentiate x^2 + 3x" → Math solver

"What's the time in Tokyo?" → Time API

"Tell me about World War 2" → Wikipedia fallback

"Give me a meal plan for today" → Meal API

"What's the weather in Nairobi?" → Weather API

How Routing Works
Fred uses intent detection through keywords/phrases and natural regex patterns to route user input to:

A specialized API handler if intent matches (e.g., math, movie)

The Gemini Flash model if it's general or ambiguous

Wikipedia if all other APIs return None or don't match

To-Do / Ideas
 Add voice input and speech output

 Improve intent classification using ML

 Add local user profile & memory

 Export conversations as PDF or text

 Mobile version with PyQt6 or Kivy

Tips
Fred is modular: you can plug in more APIs easily.

Use the response formatter functions to unify UI output.

Use Gemini Flash only as the final fallback to save on API usage.

 License
MIT License © 2025 Kakilel Chebarwett