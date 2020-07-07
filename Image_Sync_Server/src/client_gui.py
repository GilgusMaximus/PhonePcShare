import threading
import tkinter as tk
import time
#import src.client as client

USER_DEFINED_STORE_PATH = "../c_files/"
WAIT_TO_SYNC_TIME = 10


# adds the received files to the history and deletes any over the maximum displayable size of the listbox
def add_elements_to_receive_history(file_names, list_box):
    size = list_box.size()
    # delete the old entries
    if size == 18:
        for i in range(0, len(file_names)):
            list_box.delete(size-1)
            size -= 1
    # add the new entries
    for file in file_names:
        list_box.insert(0, file)


# function that is run in a new thread
def run(lb_tops):
    print(lb_tops.size())
    time_counter = 0
    while True:
        print("running...")
        # check for incoming files
        if time_counter == WAIT_TO_SYNC_TIME:
            time_counter = 0
        # used for waiting WAIT_TO_SYNC_TIME seconds, except when the user wants to send files, then it should also perform that
        else:
            time.sleep(1)
            time_counter += 1


window = tk.Tk()
window.title("PcPhoneShare-Client")
window.geometry("400x600+0+0")
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

lb_right.insert(2, "PP")
lb_right.insert(3, "PERL")
lb_top.insert(0, "d8e5er" + str(0))
f1.grid(column=1, row=0, sticky=tk.W+tk.N+tk.E+tk.S)
f1.columnconfigure(0, weight=1)
f1.rowconfigure(1, weight=1)
top_label.grid(column=0, row=0, sticky=tk.W+tk.N+tk.E+tk.S)
lb_top.grid(column=0, row=1, sticky=tk.W+tk.N+tk.E+tk.S)
lb_right.grid(column=1, sticky=tk.W+tk.N+tk.E+tk.S)
thread = threading.Thread(target=run, args=(lb_top,))
thread.start()
lb_right.delete(0)
lb_right.insert(0, "HANS")
window.mainloop()
#while True:
#    window.update_idletasks()
#    window.update()
#    if mainf != vorher:
#        print("MAIN", mainf)
#        vorher = mainf
#    window.after(10000, printsmth())