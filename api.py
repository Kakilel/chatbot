import google.generativeai as genai
import os
import json
import datetime

genai.configure(api_key="AIzaSyCM10Ct_FKnlz37MRazEhEOEDkjywU8_cQ")

today_str = datetime.date.today().isoformat()
LOG_FILE = f"chat_log_{today_str}.json"

day_log = []
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        try:
            day_log = json.load(f)
        except json.JSONDecodeError:
            print("Warning: chat_log.json is corrupted. Starting fresh.")
            day_log = []
else:
    day_log=[]
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f)

# === Menu ===
def show_menu():
    print('\n === Chatbot Menu ===')
    print('1. View all session IDs')
    print('2. View session messages')
    print('3. Start new chat session')
    print('4. Continue session')
    print('5. Delete session')
    print('6. Exit')
    return input('Choose an option (1-6): ').strip()

def sessions():
    if not day_log:
        print('\nNo sessions for today.\n')
        return
    print(f'\n --- Sessions for {today_str} ---')
    for i, session in enumerate(day_log, 1):
        name = session.get('name','Unnamed')
        print(f'{i}. Session ID: {session["session_id"]}')
    print('-----------------------')

def view_session_messages():
    if not day_log:
        print('No sessions found.')
        return
    sessions()
    try:
        idx = int(input('Enter session number to view: ').strip()) - 1
        session = day_log[idx]
        print(f'\n--- Session: {session["session_id"]} ---')
        for msg in session['messages']:
            print(f'[{msg["timestamp"]}]\nYou: {msg["user_message"]}\nBot: {msg["bot_response"]}\n')
            print('-------------------------\n')
    except (ValueError, IndexError):
        print('Invalid selection.\n')

def continue_session():
    if not day_log:
        print("No sessions to continue.\n")
        return
    sessions()
    try:
        idx = int(input("Enter the session number to continue: ").strip()) - 1
        session = day_log[idx]
        chat_loop(session)
    except (ValueError, IndexError):
        print("Invalid selection.\n")


def delete_session():
    if not day_log:
        print("No sessions available to delete.\n")
        return

    print("Available sessions:")
    for idx, session in enumerate(day_log, start=1):
        print(f"{idx}. {session.get('name','Unnamed')}(ID:{session['session_id']})")

    try:
        choice = int(input("Enter the number of the session to delete: ").strip())
        if 1 <= choice <= len(day_log):
            session = day_log[choice - 1]
            confirm = input(f"Are you sure you want to delete session '{session}'? (yes/no): ").strip().lower()
            if confirm == 'yes':
                del day_log[choice - 1]
                save_log()
                print(f"Session {session} deleted.\n")
            else:
                print("Deletion cancelled.\n")
        else:
            print("Invalid selection.\n")
    except ValueError:
        print("Invalid input. Please enter a number.\n")


def save_log():
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(day_log, f, indent=4, ensure_ascii=False)

def start_new_session():
    session_name = input("Enter a name for this session (e.g. 'Weather Chat'): ").strip()
    if not session_name:
        session_name = 'Untitled Session'
    session_id = datetime.datetime.now().isoformat(timespec='seconds')
    new_session = {
        'session_id': session_id,
        'messages': []
    }
    day_log.append(new_session)
    save_log()
    return new_session
def chat_loop(session):
    model = genai.GenerativeModel(
        model_name='gemini-2.5-flash',
        generation_config=genai.GenerationConfig(
            temperature=0.5,
            max_output_tokens=568
        )
    )

    chat = model.start_chat()
    print(f"\n--- New Chat Session Started: {session['session_id']} ---")
    print("Type 'exit' to end session.\n")

    while True:
        user = input("You: ").strip()

        if not user:
            print("Please type something.")
            continue

        if user.lower() in ["exit", "quit"]:
            print("Session ended.\n")
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
                bot_reply = response.text.strip()
                print("Bot:", bot_reply)

                session['messages'].append({
                    'timestamp': datetime.datetime.now().isoformat(),
                    'user_message': user,
                    'bot_response': bot_reply
                })
                save_log()
            else:
                print("No valid response. Chat will reset.")
                chat = model.start_chat()
        except Exception as e:
            print("Error:", str(e).strip())
            if "contents.parts must not be empty" in str(e):
                chat = model.start_chat()

# === Menu Loop ===
while True:
    choice = show_menu()
    if choice == '1':
        sessions()
    elif choice == '2':
        view_session_messages()
    elif choice == '3':
        start_new_session()
    elif choice == '4':
        continue_session()    
    elif choice == '5':
        delete_session()    
    elif choice == '6':
        print("Goodbye!")
        break
    else:
        print("Invalid option. Try again.")
