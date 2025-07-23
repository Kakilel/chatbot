import google.generativeai as genai

genai.configure(api_key="AIzaSyCM10Ct_FKnlz37MRazEhEOEDkjywU8_cQ")

model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    generation_config=genai.GenerationConfig(
        temperature=0.5,
        max_output_tokens=256
    )
)

chat = model.start_chat()
print("Gemini Chatbot (type 'exit' to quit)")

while True:
    user = input("You: ").strip()

    if not user:
        print("Please type something.")
        continue

    if user.lower() in ["exit", "quit"]:
        print("Chat ended.")
        break

    try:
        response = chat.send_message(user)
        if (
            response is not None and
            hasattr(response, "candidates") and
            response.candidates and
            response.candidates[0].content.parts and
            hasattr(response, "text") and
            response.text
        ):
            print("Bot:", response.text.strip())
        else:
            print("No valid response. Chat will reset to avoid crash.")
            chat = model.start_chat()
    except Exception as e:
        print("Error:", str(e).strip())
        if "contents.parts must not be empty" in str(e):
            chat = model.start_chat()
