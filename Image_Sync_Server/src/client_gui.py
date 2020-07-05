import threading
import tkinter as tk
import time
#import src.client as client

# function that is run in a new thread
def run():
    global mainf
    while True:
        mainf += 1
        print("running...", mainf)
        time.sleep(5)


window = tk.Tk()
window.title("PcPhoneShare-Client")
window.geometry("400x600+0+0")

greeting = tk.Label(text="Welcome to the PCPhoneShare application :)",
                    width = 100,
                    height = 30,
                    font=("Arial", 15),
                    )
greeting.pack()
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