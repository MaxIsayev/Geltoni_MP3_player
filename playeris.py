from pygame import *
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import time
from threading import *

### LISTS AND VARIABLES
playlist = []
wasstarted = False
volume = 0.3
treble = 0
bass = 0
totallength = 0
quitthreading = False
slider_moved = False
playing = False

mixer.init()
player = mixer.music
player.set_volume(volume)

class Music:
    def __init__(self, file):
        self.file = file
        name = file.split("/")
        self.name = name[-1]

def AddToList(musicobj):
    listsize = music_list.size() + 1
    music_list.insert(listsize, musicobj.name)
    playlist.append(musicobj)

def OpenFile():
    try:
        filename = filedialog.askopenfilenames(initialdir="/",
                                               title="Select a File",
                                               filetypes=(('MP3 Files', '*.mp3'), ('M3U Files', '*.m3u'), ('Flac Files', '*.flac')))
        if (filename == ""):
            return
        for files in filename:
            music = Music(files)
            AddToList(music)
    except:
        print("OpenFile error.")

def Sound():
    soundpanel = Toplevel()
    soundpanel.geometry("220x150")
    soundpanel.resizable(False, False)
    treble_slider = Scale(soundpanel, from_=-10, to=10, orient=HORIZONTAL, command=TrebleChanger, length=200, label="Treble")
    treble_slider.set(treble)
    treble_slider.pack()
    bass_slider = Scale(soundpanel, from_=-10, to=10, orient=HORIZONTAL, command=BassChanger, length=200, label="Bass")
    bass_slider.set(bass)
    bass_slider.pack()

def TrebleChanger(value):
    global treble
    treble = int(value)
    mixer.music.set_volume(volume)
    player.set_volume(volume, treble/10, bass/10)

def BassChanger(value):
    global bass
    bass = int(value)
    mixer.music.set_volume(volume)
    player.set_volume(volume, treble/10, bass/10)

def Previous():
    try:
        for i in music_list.curselection():
            nextmusic = i - 1
            if (nextmusic < 0):
                nextmusic = music_list.size() - 1
                music_list.selection_clear(0, END)
                music_list.activate(nextmusic)
                music_list.selection_set(nextmusic)
                player.load(playlist[nextmusic].file)
                player.play()
                UpdateTime()
        music_list.selection_clear(0, END)
        music_list.activate(nextmusic)
        music_list.selection_set(nextmusic)
        player.load(playlist[nextmusic].file)
        player.play()
        UpdateTime()
    except:
        nextmusic = music_list.size() - 1
        music_list.selection_clear(0, END)
        music_list.activate(nextmusic)
        music_list.selection_set(nextmusic)
        player.load(playlist[nextmusic].file)
        player.play()
        UpdateTime()

def Back():
    try:
        for i in music_list.curselection():
            nextmusic = i - 1
            if (nextmusic < 0):
                nextmusic = music_list.size() - 1
                music_list.selection_clear(0, END)
                music_list.activate(nextmusic)
                music_list.selection_set(nextmusic)
                player.load(playlist[nextmusic].file)
                player.play()
                UpdateTime()
        music_list.selection_clear(0, END)
        music_list.activate(nextmusic)
        music_list.selection_set(nextmusic)
        player.load(playlist[nextmusic].file)
        player.play()
        UpdateTime()
    except:
        nextmusic = music_list.size() - 1
        music_list.selection_clear(0, END)
        music_list.activate(nextmusic)
        music_list.selection_set(nextmusic)
        player.load(playlist[nextmusic].file)
        player.play()
        UpdateTime()

def PlaySelected(self):
    global wasstarted
    global player
    selected_music = music_list.curselection()
    selected_music = selected_music[0]
    player.load(playlist[selected_music].file)
    player.play()
    player.set_volume(volume)
    wasstarted = True

    UpdateTime()

def Play():
    global wasstarted
    global player
    global playing
    if (wasstarted == False):
        selected_music = music_list.curselection()
        try:
            selected_music = selected_music[0]
        except:
            messagebox.showwarning("Music", "Choose a song from the list!")

        player.load(playlist[selected_music].file)
        player.play()
        player.set_volume(volume)
        UpdateTime()
        wasstarted = True
        UpdateTime()
    else:
        playing = True
        player.unpause()
        play_button.place_forget()

def Pause():
    global playing
    playing = False
    player.pause()
    pause_button.place_forget()

def Stop():
    global wasstarted
    global playing
    if wasstarted == True:
        pause_button.place_forget()
        wasstarted = False
        player.stop()
        playing = False

def Forward():
    try:
        for i in music_list.curselection():
            nextmusic = i + 1
        music_list.selection_clear(0, END)
        music_list.activate(nextmusic)
        music_list.selection_set(nextmusic)
        player.load(playlist[nextmusic].file)
        player.play()
        UpdateTime()
    except:
        nextmusic = 0
        music_list.selection_clear(0, END)
        music_list.activate(nextmusic)
        music_list.selection_set(nextmusic)
        player.load(playlist[nextmusic].file)
        player.play()
        UpdateTime()


def Next():
    try:
        for i in music_list.curselection():
            nextmusic = i + 1
        music_list.selection_clear(0, END)
        music_list.activate(nextmusic)
        music_list.selection_set(nextmusic)
        player.load(playlist[nextmusic].file)
        player.play()
        UpdateTime()
    except:
        nextmusic = 0
        music_list.selection_clear(0, END)
        music_list.activate(nextmusic)
        music_list.selection_set(nextmusic)
        player.load(playlist[nextmusic].file)
        player.play()
        UpdateTime()

def UpdateTime():
    global player
    global totallength
    global playing
    selected_music = music_list.curselection()
    selected_music = selected_music[0]
    total_length = mixer.Sound(playlist[selected_music].file).get_length()

    conv_total_length = time.strftime('%M:%S', time.gmtime(total_length))
    end_song_time.config(text=conv_total_length)
    slider.config(to=int(total_length))
    pos.set(0)
    playing = True
    if update.is_alive() == False:
        update.start()

def UpdateSlider():
    global player
    global totallength
    while True:
        if playing == True:
            if slider_moved == True:
                pos.set(slider.get() + 1)
                conv_total_length = time.strftime('%M:%S', time.gmtime(int(slider.get())))
                current_song_time.config(text=conv_total_length)
            else:
                current_time = player.get_pos() / 1000
                conv_total_length = time.strftime('%M:%S', time.gmtime(current_time))
                current_song_time.config(text=conv_total_length)
                pos.set(int(current_time))
            slider.config(variable=pos)
            time.sleep(1)
            if quitthreading == True:
                break

def FastForward(self):
    global slider_moved
    pos.set(self)
    player.play(start=int(self))
    slider_moved = True

def CloseWindow():
    global quitthreading
    quitthreading = True
    player.stop()
    master.destroy()

master = Tk()
master.title("Geltonuju Grotuvas")
master.protocol("WM_DELETE_WINDOW", CloseWindow)
master.geometry("500x500")
master.resizable(False, False)
update = Thread(target=UpdateSlider)
pos = IntVar()

previous_img = PhotoImage(file="previous_button.PNG")
previous_button = Button(master, image=previous_img, command=Previous)
back_img = PhotoImage(file="backward_button.PNG")
back_button = Button(master, image=back_img, command=Back)
play_img = PhotoImage(file="play_button.PNG")
play_button = Button(master, image=play_img, command=Play)
pause_img = PhotoImage(file="pause_button.PNG")
pause_button = Button(master, image=pause_img, command=Pause)
stop_img = PhotoImage(file="stop_button.PNG")
stop_button = Button(master, image=stop_img, command=Stop)
forward_img = PhotoImage(file="forward_button.PNG")
forward_button = Button(master, image=forward_img, command=Forward)
next_img = PhotoImage(file="next_button.PNG")
next_button = Button(master, image=next_img, command=Next)
add_img = PhotoImage(file="add_button.PNG")
add_button = Button(master, image=add_img, command=OpenFile)
sound_img = PhotoImage(file="eq_button.PNG")
sound_button = Button(master, image=sound_img, command=Sound)
current_song_time = Label(master, text="00:00")
end_song_time = Label(master, text="00:00")
slider = Scale(master, from_=0, to=100, orient=HORIZONTAL, command=FastForward, showvalue=False, length=315, variable=pos)

music_list = Listbox(master, font=("davish"), width=53, height=11, selectmode=SINGLE)
music_list.place(x=10, y=10)
add_button.place(x=10, y=250)
previous_button.place(x=50, y=500)
back_button.place(x=100, y=500)
play_button.place(x=150, y=500)
pause_button.place(x=200, y=500)
stop_button.place(x=250, y=500)
forward_button.place(x=300, y=500)
next_button.place(x=350, y=500)
sound_button.place(x=450, y=500)
current_song_time.place(x=50, y=400)
end_song_time.place(x=410, y=400)
slider.place(x=85, y=400)

music_list.bind("<<ListboxSelect>>", PlaySelected)
mainloop()