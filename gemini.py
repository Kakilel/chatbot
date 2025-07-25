import google.generativeai as genai
import datetime

# Configure Gemini API key
genai.configure(api_key="AIzaSyCM10Ct_FKnlz37MRazEhEOEDkjywU8_cQ")  # ← Replace with your real key

# Initialize model and persistent chat
model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    generation_config=genai.GenerationConfig(
        temperature=0.5,
        max_output_tokens=2500
    )
)
chat = model.start_chat()

# Core Gemini message handler
def send_to_session(session, user_message):
    try:
        response = chat.send_message(user_message)
        if (
            response and
            hasattr(response, "candidates") and
            response.candidates and
            response.candidates[0].content.parts and
            hasattr(response, "text") and
            response.text
        ):
            return response.text.strip()
        else:
            return "No valid response from Gemini AI."
    except Exception as e:
        return f"Error: {str(e).strip()}"
