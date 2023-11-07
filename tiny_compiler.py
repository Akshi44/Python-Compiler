# library for GUI 
from tkinter import  *
from tkinter.filedialog import asksaveasfilename   # save_As
from tkinter.filedialog import askopenfilename     # open_file
import subprocess                                  # for self terminal
import time                                        # execution time
import webbrowser                                  # help
import smtplib                                     # share
import pywhatkit as kit                            # share_via_whatsapp
import datetime                      
from tkinter import ttk                            # multiple tab
compiler=Tk()

# Set the background color
compiler.configure(bg='lightblue')
# compiler.configure(height=100%, width=100%)
# # Get the screen width and height
# screen_width = compiler.winfo_screenwidth()
# screen_height = compiler.winfo_screenheight()
# # Set the compiler window size to match the screen size
# compiler.geometry(f"{screen_width}x{screen_height}")

# project title 
compiler.title('Python compiler')
file_path=''

# -------------------------------------------set file path-----------------------------------
def set_file_path(path):
    global file_path
    file_path=path

# ------------------------------------implementation of run function--------------------------
def run():
    # in self terminal
    # D:\Python Project\Experiments
    if file_path=='':
        save_prompt=Toplevel()
        text=Label(save_prompt,text='please save your code,before compiling')
        text.pack()
        return
    start_time = time.time()
    command= f'Python {file_path}'
    process=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True )
    output, error=process.communicate()
    end_time = time.time()
    execution_time = end_time - start_time
    code_output.delete('1.0', 'end')
    if output:
        code_output.insert('end', "Output:\n")
        code_output.insert('end', output.decode())
        code_output.insert('end', f"Execution time: {execution_time:.5f} seconds\n")
    if error:
        code_output.insert('end', "Error:\n")
        code_output.insert('end', error.decode())
        code_output.insert('end', f"Execution time: {execution_time:.5f} seconds\n")
    # in vscode terminal
    # code=editor.get('1.0',END)
    # exec(code)
# ------------------------------------implementation of help function--------------------------
def help():
    webbrowser.open('https://docs.python.org/3/')

# ------------------------------------implementation of share function--------------------------
def share_via_whatsapp():
    message = editor.get("1.0", "end-1c")  # Get the code from the editor
    phone_number = "+91123456789"  # Replace with the recipient's phone number
    current_time = datetime.datetime.now()
    send_time = current_time + datetime.timedelta(minutes=1)  # Send the message after 1 minute

    kit.sendwhatmsg(phone_number, message, send_time.hour, send_time.minute)

def share_code():
    # Prompt the user to select the code file to share
    file_to_share = askopenfilename(filetypes=[('Python Files', '*.py')])

    # Check if a file was selected
    if file_to_share:
        # Set up the email server and credentials
        email_server = 'smtp.example.com'
        email_port = 587
        sender_email = 'your_email@example.com'
        sender_password = 'your_password'
        receiver_email = 'receiver@example.com'

        # Create an SMTP connection
        with smtplib.SMTP(email_server, email_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)

            # Read the code from the selected file
            with open(file_to_share, 'r') as file:
                code = file.read()

            # Compose the email message
            subject = 'Shared Python Code'
            message = f"Here is the Python code:\n\n{code}"

            # Send the email
            server.sendmail(sender_email, receiver_email, f'Subject: {subject}\n\n{message}')

        print("Code shared via email successfully!")

# ------------------------------------implementation menu bar ---------------------------------
# menubar 
menu_bar=Menu(compiler)
file_bar=Menu(menu_bar,tearoff=0)     # tearoff=0, removes(----)
run_bar=Menu(menu_bar,tearoff=0)     # tearoff=0, removes(----)
help_bar=Menu(menu_bar,tearoff=0)     # tearoff=0, removes(----)
share_bar=Menu(menu_bar,tearoff=0)     # tearoff=0, removes(----)

#-------------------------------------------for File,Run menu bar---------------------------
menu_bar.add_cascade(label='File',menu=file_bar)
#-----------------------------------------------RUN------------------------------------------
# Run named function option 
run_bar.add_command(label='Run',command=run )  # run function
menu_bar.add_cascade(label='Run',menu=run_bar)
#-------------------------------------------Help----------------------------------------------
# Help named function option 
help_bar.add_command(label='Help',command=help)  # help function
menu_bar.add_cascade(label='Help',menu=help_bar)
#-------------------------------------------Share----------------------------------------------
# Share named function option 
share_bar.add_command(label='Share via Email',command=share_code)  # help function
share_bar.add_command(label="Share via WhatsApp", command=share_via_whatsapp)  # Add this option
menu_bar.add_cascade(label="Share", menu=share_bar)

#-----------------------------------------Display this menu options---------------------------
# display bar option 
compiler.config(menu=menu_bar)
# this compiler is editable, we can write text over there
editor=Text(undo=True, fg='black',font=14)
editor.pack()
# for self compiler
code_output=Text(height=15, fg='black',font=14)
code_output.pack()
# give background color
editor.configure(bg='silver')
editor.configure(width=180)
code_output.configure(bg='silver')
code_output.configure(width=180,height=100)


# Run named function option 
# implementation of open_file function
#-------------------------------------------openfile---------------------------------------
def open_file():
    path=askopenfilename(filetypes=[('Python Files','*.py')])
    with open(path,'r')as file:
        code=file.read()
        editor.delete('1.0',END)
        editor.insert('1.0',code)
        set_file_path(path)
file_bar.add_command(label='Open',command=open_file)  # run function
#-------------------------------------------save_as----------------------------------------
# implementation of save_as function
def save_as():
    if file_path=='':
        path=asksaveasfilename(filetypes=[('Python Files','*.py')])
    else:
        path=file_path
    with open(path,'w')as file:
        code=editor.get('1.0',END)
        file.write(code)
        set_file_path(path) 
file_bar.add_command(label='Save',command=save_as )  # run function
file_bar.add_command(label='Save As',command=save_as )  # run function
file_bar.add_command(label='Exit',command=exit)  # run function

#---------------------------------------undo-redo-------------------------------------------
def undo():
    try:
        editor.edit_undo()
    except TclError:
        pass

def redo():
    try:
        editor.edit_redo()
    except TclError:
        pass

compiler.mainloop()

