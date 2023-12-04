import tkinter as tk
from tkinter import filedialog,ttk
from tkinter import *
import os, shutil, subprocess
from moviepy.editor import VideoFileClip

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

def compress_video():
    global compress_file
    if input_video:
        temp_file = "temp.mp4"
        video = input_video
        
        wait_label = tk.Label(root, text="Aguarde, pode demorar um pouco...", bg='#1b2838', fg='white')
        wait_label.place(x=200, y=300)
        root.update()
        
        command = f"{ffmpeg_path} -i \"{input_video}\" -c:v libx265 -s 640x360 -crf 28 -c:a copy \"{temp_file}\""
        subprocess.call(command, shell=True)
        
        video_clip = VideoFileClip(temp_file)
        video_clip.write_videofile(video)
        os.remove(temp_file)
        compress_file = video
        
        wait_label.destroy()
        show_video()
        
def show_video():
    def download_video():
        if compress_file:
            save_file = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("Arquivo de Vídeo", "*.mp4")])
            if save_file:
                save_file = save_file[:-4] + "_VD.mp4"
                shutil.copy(compress_file, save_file)
                success_label = tk.Label(root, text="Vídeo baixado com sucesso.")
                success_label.pack()
    download_button = tk.Button(text="Baixar", command=download_video)
    download_button.configure(foreground='white', background='#2a475e', font=('Arial', 8, 'bold'), relief='raised')
    download_button.place(x=200, y=260, width=300, height=30)

root = tk.Tk()
root.title("VD - Conversor de Vídeo")
root.geometry("700x400")
root.configure(background='#1b2838')

input_video = ""
compress_file = ""

program_directory = os.path.dirname(os.path.abspath(__file__))
ffmpeg_directory = os.path.join(program_directory, "ffmeg", "bin")
ffmpeg_path = os.path.join(ffmpeg_directory, "ffmpeg.exe")

video_infoN = tk.Label(text="", bg='#1b2838', fg='white')
video_infoS = tk.Label(text="", bg='#1b2838', fg='white')
video_infoN.place(x=200, y=50)
video_infoS.place(x=200, y=110)


select_button = tk.Button(text="Selecionar Vídeo", command=select_file)
select_button.configure(foreground='white', background='#2a475e', font=('Arial', 8, 'bold'), relief='raised')
select_button.place(x=20, y=20, width=120, height=200)

compress_button = tk.Button(text="Comprimir", command=compress_video)
compress_button.configure(foreground='white', background='#2a475e', font=('Arial', 8, 'bold'), relief='raised')
compress_button.place(x=200, y=220, width=300, height=30)

profile_label = tk.Label(text="Perfil de Compactação")
profile_label.place(x=20, y=280)
profile_combobox = ttk.Combobox(values=["Alta Qualidade(Padrão)", "Baixa Qualidade", "Personalizado"])
profile_combobox.place(x=160, y=280)



root.mainloop()
