def select_file():
    global input_video
    input_video = filedialog.askopenfilename(filetypes=[("Arquivo de Vídeo", "*.mp4")])
    video_name = os.path.basename(input_video)
    if len(video_name) > 20:
        video_name = video_name[:20] + "..."
    video_size = os.path.getsize(input_video) / (1024 * 1024)
    
    video_infoN.config(text=f"Nome do Vídeo: {video_name}")
    video_infoS.config(text=f"Tamanho do Vídeo: {video_size:.2f} MB")
    
    cancel_button = tk.Button(text="Cancelar")
    cancel_button.config(command=lambda: cancel_compression(cancel_button))
    cancel_button.configure(foreground='white', background='#2a475e', font=('Arial', 8, 'bold'), relief='raised')
    cancel_button.place(x=520, y=220, width=120, height=30)

def cancel_compression(cancel_button):
    global input_video
    input_video = ""  
    video_infoN.config(text="")
    video_infoS.config(text="")
    cancel_button.destroy()