import threading
import tkinter as tk
import time
#import src.client as client

USER_DEFINED_STORE_PATH = "../c_files/"

# function that is run in a new thread
def run():
    global mainf
    while True:
        mainf += 1
        print("running...", mainf)
        time.sleep(5)


window = tk.Tk()
window.title("PcPhoneShare-Client")
window.geometry("500x750+0+0")
window.pack_propagate(0)
window.resizable(0, 0)
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)


window.rowconfigure(0, weight=1)
window.rowconfigure(1, weight=1)

greeting = tk.Label(text="Welcome to the PCPhoneShare application :)",
                    font=("Arial", 5),
                    background='red',
                    height=100
                    )
greeting3 = tk.Label(text="Welcome to the PCPhoneShare application :)",
                    font=("Arial", 5),
                    background='blue',
                    )


#greeting3.grid(column=1, row=0, sticky=tk.W+tk.N+tk.E+tk.S)
#greeting.grid(column=0, row=0, sticky=tk.W+tk.N+tk.E+tk.S)
f1 = tk.Frame(window)
lb_right = tk.Listbox(window, bd=0, highlightcolor="red", highlightthickness=0)
top_label = tk.Label(f1, text="Download history", font=("Arial", 10), background='green')
lb_top = tk.Listbox(f1, bd=0, highlightcolor="red", highlightthickness=0, background="blue")
lb_right.insert(1, "python")
lb_right.insert(2, "PERL")
lb_top.insert(1, "d8e5er")
f1.grid(column=1, row=0, sticky=tk.W+tk.N+tk.E+tk.S)
f1.columnconfigure(0, weight=1)
f1.rowconfigure(1, weight=1)
top_label.grid(column=0, row=0, sticky=tk.W+tk.N+tk.E+tk.S)
lb_top.grid(column=0, row=1, sticky=tk.W+tk.N+tk.E+tk.S)
lb_right.grid(column=1, sticky=tk.W+tk.N+tk.E+tk.S)
thread = threading.Thread(target=run)
thread.start()

window.mainloop()
#while True:
#    window.update_idletasks()
#    window.update()
#    if mainf != vorher:
#        print("MAIN", mainf)
#        vorher = mainf
#    window.after(10000, printsmth())