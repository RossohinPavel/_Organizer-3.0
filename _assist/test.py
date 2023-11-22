import customtkinter as tk


root = tk.CTk()

frame = tk.CTkScrollableFrame(master=root)
frame.pack()


for i in range(20):
    tk.CTkButton(master=frame, text=f'tesx{i}').pack()



root.mainloop()