import threading
import tkinter as tk
import time
import src.client as client
from tkinter import filedialog

USER_DEFINED_STORE_PATH = "../client_files/"
WAIT_TO_SYNC_TIME = 10
SEND_PRESSED = False


# adds the received files to the history and deletes any over the maximum displayable size of the listbox
def add_elements_to_list_box(file_names, list_box):
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
    time_counter = WAIT_TO_SYNC_TIME
    client.setup_client()
    while True:
        print("running...")
        # check for incoming files
        if time_counter == WAIT_TO_SYNC_TIME:
            time_counter = 0
            new_files = client.update_download_client_list()
            # if the client actually downloaded some files, then the UI has to update
            if len(new_files) > 0:
                add_elements_to_list_box(new_files, lb_tops)
        # used for waiting WAIT_TO_SYNC_TIME seconds, except when the user wants to send files, then it should also perform that
        else:
            if SEND_PRESSED:
                client.file_send_setup(None, None, None)
            time_counter += 1
            time.sleep(1)


def open_file_dialog(event):
    global lb_right
    filenames = filedialog.askopenfilenames(initialdir="C:/")
    add_elements_to_list_box(filenames, lb_right)
    print(filenames)


# thanks to mmgp for the example usage of nearest function https://stackoverflow.com/a/14863758
def delete_send_list_box_item_on_click(event):
    widget = event.widget
    index = widget.nearest(event.y)
    lb_right.delete(index)

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
                    )


#greeting3.grid(column=1, row=0, sticky=tk.W+tk.N+tk.E+tk.S)
#greeting.grid(column=0, row=0, sticky=tk.W+tk.N+tk.E+tk.S)
f1 = tk.Frame(window)
f2 = tk.Frame(window)
lb_right = tk.Listbox(f2, bd=0, highlightcolor="red", highlightthickness=0)
top_label = tk.Label(f1, text="Download history", font=("Arial", 10), background='green')
lb_top = tk.Listbox(f1, bd=0, highlightcolor="red", highlightthickness=0, )
mid_label = tk.Label(f2, text="Click here to add files", font=("Arial", 10), background='green')


lb_right.bind("<ButtonRelease-1>", delete_send_list_box_item_on_click)
mid_label.bind("<Button-1>", open_file_dialog)

lb_right.insert(1, "python")

lb_right.insert(2, "PP")
lb_right.insert(3, "PERL")
lb_top.insert(0, "d8e5er" + str(0))
f1.grid(column=1, row=0, sticky=tk.W+tk.N+tk.E+tk.S)
f1.columnconfigure(0, weight=1)
f1.rowconfigure(1, weight=1)
f2.grid(column=1, row=1, sticky=tk.W+tk.N+tk.E+tk.S)
f2.columnconfigure(0, weight=1)
f2.rowconfigure(1, weight=1)
top_label.grid(column=0, row=0, sticky=tk.W+tk.N+tk.E+tk.S)
lb_top.grid(column=0, row=1, sticky=tk.W+tk.N+tk.E+tk.S)
mid_label.grid(row=0, sticky=tk.W+tk.N+tk.E+tk.S)
lb_right.grid(column=0, row=1, sticky=tk.W+tk.N+tk.E+tk.S)
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