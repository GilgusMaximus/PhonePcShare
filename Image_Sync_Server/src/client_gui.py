import threading
import tkinter as tk
import time
import src.client as client
from tkinter import filedialog

USER_DEFINED_STORE_PATH = "../client_files/"
WAIT_TO_SYNC_TIME = 10
SEND_PRESSED = False

current_selected_client = -1
selected_files_to_send = []
selected_file_to_send_names = []

# adds the received files to the history and deletes any over the maximum displayable size of the listbox
def add_elements_to_list_box(element_list, list_box):
    # add the new entries
    for element in element_list:
        list_box.insert(0, element)


def clear_all_elements_from_list(list_box):
    for i in range(0, list_box.size()):
        list_box.delete(i)


def send_button_clicked(event):
    global SEND_PRESSED
    SEND_PRESSED = True


# function that is run in a new thread
def run(lb_tops):
    global SEND_PRESSED
    print(lb_tops.size())
    time_counter = WAIT_TO_SYNC_TIME
    client.setup_client("Dieter")
    while True:
        print("running...")
        # check for incoming files
        if time_counter == WAIT_TO_SYNC_TIME:
            time_counter = 0
            new_files, client_list = client.update_download_client_list()
            print("CLIENTLIST: ", client_list)
            # if the client actually downloaded some files, then the UI has to update
            if len(client_list) > 0:
                clear_all_elements_from_list(lb_tops)
                add_elements_to_list_box(client_list, lb_tops)
        # used for waiting WAIT_TO_SYNC_TIME seconds, except when the user wants to send files, then it should also perform that
        else:
            if SEND_PRESSED:
                print("Pressed send")
                if current_selected_client > 0 and len(selected_file_to_send_names) == len(selected_files_to_send) > 0:
                    print("Passed checK")
                    client.file_send_setup(selected_files_to_send, selected_file_to_send_names, current_selected_client)
                clear_all_elements_from_list(lb_right)
                selected_files_to_send.clear()
                SEND_PRESSED = False
            time_counter += 1
            time.sleep(1)


def open_file_dialog(event):
    global lb_right
    global selected_file_to_send_names
    # array used for display and sending the filenames only
    filenames = filedialog.askopenfilenames(initialdir="C:/")
    # the array 'selected_files_to_send' will be used for actually sending the files
    for file in filenames:
        selected_files_to_send.append(file)
        file_path_array = file.split("/")
        selected_file_to_send_names.append(file_path_array[len(file_path_array)-1])

    add_elements_to_list_box(selected_file_to_send_names, lb_right)
    print(filenames)


# thanks to mmgp for the example usage of nearest function https://stackoverflow.com/a/14863758
def delete_send_list_box_item_on_click(event):
    global lb_right
    if lb_right.size() == 0:
        return
    widget = event.widget
    index = widget.nearest(event.y)
    # [x, y, width, height]
    element_coords = lb_right.bbox(index)
    # prevents deleting the last list element when clicking in the empty space below it ion the list box
    if element_coords[3]+element_coords[1] > event.y > element_coords[1]:
        lb_right.delete(index)


# thanks to mmgp for the example usage of nearest function https://stackoverflow.com/a/14863758
def select_recipient(event):
    global lb_top
    if lb_top.size() == 0:
        return
    widget = event.widget
    index = widget.nearest(event.y)
    # [x, y, width, height]
    element_coords = lb_top.bbox(index)
    # prevents deleting the last list element when clicking in the empty space below it ion the list box
    if element_coords[3] + element_coords[1] > event.y > element_coords[1]:
        current_selected_recipient = index


window = tk.Tk()
window.title("PcPhoneShare-Client")
window.geometry("400x600+0+0")
window.pack_propagate(0)
window.resizable(0, 0)
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)


window.rowconfigure(0, weight=1)
window.rowconfigure(1, weight=1)




#greeting3.grid(column=1, row=0, sticky=tk.W+tk.N+tk.E+tk.S)
#greeting.grid(column=0, row=0, sticky=tk.W+tk.N+tk.E+tk.S)


f3 = tk.Frame(window)
f4 = tk.Frame(window)

f3.grid(column=0, row=0, sticky=tk.W+tk.N+tk.E+tk.S)
f3.columnconfigure(0, weight=1)
f3.rowconfigure(1, weight=1)
f4.grid(column=0, row=1, sticky=tk.W+tk.N+tk.E+tk.S)
f4.columnconfigure(0, weight=1)
f4.rowconfigure(1, weight=1)


send_button = tk.Button(f4, text="Send files")
send_button.grid(column=0, row=0, sticky=tk.W+tk.E+tk.S)

f1 = tk.Frame(window)
f2 = tk.Frame(window)
lb_right = tk.Listbox(f2, bd=0, highlightcolor="red", highlightthickness=0)
top_label = tk.Label(f1, text="Select a recipient.", font=("Arial", 10), background='green')
lb_top = tk.Listbox(f1, bd=0, highlightcolor="red", highlightthickness=0, )
mid_label = tk.Label(f2, text="Click here to add files", font=("Arial", 10), background='green')


send_button.bind("<ButtonRelease-1>", send_button_clicked)

lb_top.bind("<ButtonRelease-1>", delete_send_list_box_item_on_click)

lb_right.bind("<ButtonRelease-1>", delete_send_list_box_item_on_click)
mid_label.bind("<Button-1>", open_file_dialog)

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
window.mainloop()
#while True:
#    window.update_idletasks()
#    window.update()
#    if mainf != vorher:
#        print("MAIN", mainf)
#        vorher = mainf
#    window.after(10000, printsmth())