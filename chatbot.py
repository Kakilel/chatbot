import tkinter as tk
from tkinter import simpledialog, messagebox, Listbox, Scrollbar
import api

class ChatHome:
    def __init__(self,root):
        self.root = root
        self.root.title("Fred")
        self.session = None 
        self.show_display()
        self.refresh_session_list()

    def  show_display(self):
    
    #BOX
        self.session_listbox = Listbox(self.root,width=40)
        self.session_listbox.grid(row=0,column=0,rowspan=6,padx=10,pady=10)
    
    #SCROLLBAR
        scrollbar = Scrollbar(self.root,command=self.session_listbox.yview)
        scrollbar.grid(row=0,column=1,rowspan=6,sticky='ns')
        self.session_listbox.config(yscrollcommand=scrollbar.set)   
    
    #BUTTONS
        tk.Button(self.root,text='New Session',command=self.new_session).grid(row=0,column=2,padx=10,pady=5)    
        tk.Button(self.root,text='Continue Session',command=self.continue_session).grid(row=1,column=2,padx=10,pady=5)    
        tk.Button(self.root,text='Delete Session',command=self.delete_session).grid(row=2,column=2,padx=10,pady=5)   

    #CHATBOX
        self.chat_display = tk.Text(self.root,state='disabled',width=80,height=20)    
        self.chat_display.grid(row=6,column=0,columnspan=3,padx=10)

        self.entry = tk.Entry(self.root,width=70)
        self.entry.grid(row=7,column=0,columnspan=2,padx=10,pady=10)

        tk.Button(self.root,text='Send',command=self.send_message).grid(row=7,column=2,padx=10)


    def refresh_session_list(self):
        self.session_listbox.delete(0,tk.END)
        for session in api.get_sessions():
            self.session_listbox.insert(tk.END,session['name'])


    def new_session(self):
        name = simpledialog.askstring('New Session','Enter a name for this session:')
        if name:
            self.session = api.start_session(name)
            self.chat_display.config(state='normal')             
            self.chat_display.delete('1.0',tk.END)             
            self.chat_display.config(state='disabled')
        self.refresh_session_list()

    def continue_session(self):
        idx = self.session_listbox.curselection()
        if not idx:
            messagebox.showerror('Error','Select a session to continue.')
            return
        name = self.session_listbox.get(idx)
        self.session = api.get_session_by_name(name)
        self.load_messages()


    def delete_session(self):
        idx = self.session_listbox.curselection()
        if not idx:
            messagebox.showerror('Error','Select a session to Delete.')
            return
        name = self.session_listbox.get(idx)
        confirm = messagebox.askyesno('Confirm',f'Delete session "{name}"?')
        if confirm:
            api.delete_session_by_name(name)
            self.refresh_session_list()
            self.chat_display.config(state='normal')
            self.chat_display.delete('1.0',tk.END)
            self.chat_display.config(state='disabled')

    def load_messages(self):
        self.chat_display.config(state='normal')
        self.chat_display.delete('1.0',tk.END)
        for msg in self.session['messages']:
            self.chat_display.insert(tk.END,f"You:{msg['user_message']}\n\n")        
            self.chat_display.insert(tk.END,f"Bot:{msg['bot_response']}\n\n")
        self.chat_display.config(state='disabled')


    def send_message(self):
        if not self.session:
            messagebox.showwarning('No Session','Start or continue a session first.')
            return
        user_text = self.entry.get().strip()
        if not user_text:
            return
        response = api.send_to_session(self.session,user_text)
        self.entry.delete(0,tk.END)
        self.load_messages()

if __name__ == '__main__':
    root = tk.Tk()
    app = ChatHome(root)
    root.mainloop()                        
