from pygame import *
from tkinter import *
from tkinter import Tk, Canvas, Label, Button, messagebox, filedialog
import time
from threading import *

### LISTS AND VARIABLES
playlist = []
wasstarted = False
sounds_slider = False
bass = 0
low_mid = 0
mid = 0
high_mid = 0
treble = 0
volume = 30
totallength = 0
quitthreading = False
slider_moved = False
playing = False

# Initialize mixer
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
                                               title="Select a File", filetypes=(('MP3 Files', '*.mp3'),
                                                                                 ('M3U Files', '*.m3u'),
                                                                                 ('Flac Files', '*.flac'),
                                                                                 ('Wave Files', '*.wav'),
                                                                                 ('Aiff Files', '*.aiff'),
                                                                                 ('Ogg Files', '*.ogg')))
        if (filename == ""):
            return
        for files in filename:
            music = Music(files)
            AddToList(music)
    except:
        print("OpenFile error.")

def VolumeSliderChanged(value):
    global volume
    volume = float(value) / 100
    player.set_volume(volume)

def Soundd():
    global volume
    soundslider = Scale(master, from_=0, to=100, orient=HORIZONTAL, command=VolumeSliderChanged, length=200)
    sounds_slider.set(volume * 20)
    soundslider.place(x=85, y=250)

def Mute():
    global volume
    mixer.music.set_volume(0)

def SoundChanger(self):
    global volume
    global novolume_button
    self.soundslider = int(self) / 100
    player.set_volume(volume)

def BassChanger(value):
    global bass
    bass = int(value)
    mixer.music.bass(volume)
    player.set_volume(bass/10)

def LowMidChanger(value):
    global lowmid
    lowmid = int(value)
    mixer.music.set_volume(volume)
    player.set_volume(lowmid/10)

def MidChanger(value):
    global mid
    mid = int(value)
    mixer.music.set_volume(volume)
    player.set_volume(mid/10)

def HighMidChanger(value):
    global highmid
    highmid = int(value)
    mixer.music.set_volume(volume)
    player.set_volume(highmid/10)

def TrebleChanger(value):
    global treble
    treble = int(value)
    mixer.music.set_volume(volume)
    player.set_volume(treble/10)

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

def Pause():
    global playing
    playing = False
    player.pause()

def Stop():
    global wasstarted
    global playing
    if wasstarted == True:
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
    global player, totallength, playing, slider_moved, quitthreading
    while True:
        if playing:
            if slider_moved:
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
            if quitthreading:
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

# Create the main Tkinter window
master = Tk()
master.title("Mp3 Player  - - - = YELLOW SUBMARINE v.1.01 beta = - - - ")
master.protocol("WM_DELETE_WINDOW", CloseWindow)
master.geometry("500x500")
master.resizable(False, False)

# Create the update thread
update = Thread(target=UpdateSlider)
pos = IntVar()

theme_img = PhotoImage(file="theme.png")
label1 = Label(master, image = theme_img)
label1.place(x = 0, y = 100)  

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
sound_img = PhotoImage(file="mute_button.PNG")
novolume_button = Button(master, image=sound_img, command=Mute)
current_song_time = Label(master, text="00:00")
end_song_time = Label(master, text="00:00")
slider = Scale(master, from_=0, to=100, orient=HORIZONTAL, command=FastForward, showvalue=False, length=315, variable=pos)
volume_slider = Scale(master, from_=100, to=0, orient=VERTICAL, command=VolumeSliderChanged, length=100)
volume_text = Label(master, text="Volume")
music_list = Listbox(master, font=("arial", 10), width=68, height=10, selectmode=SINGLE)
bass_slider = Scale(master, from_=10, to=-10, orient=VERTICAL, command=BassChanger, length=100)
bass_text = Label(master, text="Bass")
low_mid_slider = Scale(master, from_=10, to=-10, orient=VERTICAL, command=LowMidChanger, length=100)
low_mid_text = Label(master, text="Low Mid")
mid_slider = Scale(master, from_=10, to=-10, orient=VERTICAL, command=MidChanger, length=100)
mid_text = Label(master, text="Mid")
high_mid_slider = Scale(master, from_=10, to=-10, orient=VERTICAL, command=HighMidChanger, length=100)
high_mid_text = Label(master, text="High Mid")
treble_slider = Scale(master, from_=10, to=-10, orient=VERTICAL, command=TrebleChanger, length=100)
treble_text = Label(master, text="Treble")

music_list.place(x=10, y=10)
add_button.place(x=10, y=250)
previous_button.place(x=50, y=450)
back_button.place(x=100, y=450)
play_button.place(x=150, y=450)
pause_button.place(x=200, y=450)
stop_button.place(x=250, y=450)
forward_button.place(x=300, y=450)
next_button.place(x=350, y=450)
novolume_button.place(x=450, y=450)
current_song_time.place(x=50, y=400)
end_song_time.place(x=410, y=400)
slider.place(x=85, y=400)

# Eq section
bass_text.place(x=77, y=230)
bass_slider.place(x=60, y=250)

low_mid_text.place(x=126, y=230)
low_mid_slider.place(x=120, y=250)

mid_text.place(x=198, y=230)
mid_slider.place(x=180, y=250)

high_mid_text.place(x=243, y=230)
high_mid_slider.place(x=240, y=250)

treble_text.place(x=312, y=230)
treble_slider.place(x=300, y=250)

volume_text.place(x=400, y=230)
volume_slider.place(x=392, y=250)

music_list.bind("<<ListboxSelect>>", PlaySelected)
mainloop()