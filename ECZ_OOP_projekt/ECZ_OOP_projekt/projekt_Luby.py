from tkinter import *
from tkinter.font import Font
from tkinter import messagebox as mb
from tkinter import filedialog
import subprocess
import sys
import time

# Inicijalizacija glavnog prozora
luby = Tk()
luby.title('Luby ToDo Timer')
# Promjena ikone prozora
luby.iconbitmap('luby.ico')
luby.geometry('500x625')
luby.resizable(False, True)
luby.config(background='#a8aab2')

# Funkcije za meni
def novi():
    # Pokretanje nove instance trenutne Python skripte
    subprocess.Popen([sys.executable, __file__])
    return

def otvori():
    # Otvaranje dijaloga za odabir datoteke
    filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if filepath:
        try:
            # Čitanje sadržaja datoteke
            with open(filepath, 'r', encoding='utf-8') as file:
                zadaci = file.readlines()
            # Brisanje trenutnih zadataka u listi
            lubenice.delete(0, END)
            # Dodavanje zadataka iz datoteke u listu
            for zadatak in zadaci:
                lubenice.insert(END, zadatak.strip())
        except Exception as e: #prikaz greške ukoliko je odabrana neka druga vrsta datoteke
            mb.showerror("Greška", f"Ne mogu otvoriti datoteku: {e}")

def spremi():
    # Otvaranje dijaloga za spremanje datoteke
    filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if filepath:
        try:
            # Pisanje sadržaja liste u datoteku
            with open(filepath, 'w', encoding='utf-8') as file:
                zadaci = lubenice.get(0, END)
                for zadatak in zadaci:
                    file.write(zadatak + '\n')
            mb.showinfo("Spremljeno", "Uspješno spremljeno!")
        except Exception as e:
            mb.showerror("Greška", f"Ne mogu spremiti datoteku: {e}")

# Funkcija za izlaz
def izadji():
    odgovor = mb.askyesnocancel("Potvrdi izlaz", "Želiš li spremiti promjene?")
    if odgovor is None:
        return
    elif odgovor:
        spremi()
    luby.destroy() #funkcija koja zatvara aplikaciju nakon što korisnik odluči spremiti ili odustati


# Povezivanje funkcije izadji s događajem zatvaranja prozora (X)
luby.protocol("WM_DELETE_WINDOW", izadji)

# Stvaranje prilagođenog menija
menu_okvir = Frame(luby, bg='#6f556b', height=25)
menu_okvir.pack(side=TOP, fill=X)

# Dodavanje gumba za meni
novi_gumb = Button(menu_okvir, text="Novo", command=lambda: novi(), bg='#6f556b', fg='white', relief=RIDGE)
otvori_gumb = Button(menu_okvir, text="Otvori", command=lambda: otvori(), bg='#6f556b', fg='white', relief=RIDGE)
spremi_gumb = Button(menu_okvir, text="Spremi kao..", command=lambda: spremi(), bg='#6f556b', fg='white', relief=RIDGE)
izadji_gumb = Button(menu_okvir, text="Zatvori", command=izadji, bg='#6f556b', fg='white', relief=RIDGE)

novi_gumb.pack(side=LEFT, padx=2, pady=2)
otvori_gumb.pack(side=LEFT, padx=2, pady=2)
spremi_gumb.pack(side=LEFT, padx=2, pady=2)
izadji_gumb.pack(side=LEFT, padx=2, pady=2)

# Promjena fonta
mojFont = Font(family="Maiandra GD", size=25)

# Stvaranje okvira
okvir = Frame(luby)
okvir.pack(pady=17)

# Lista zadataka (Listbox)
lubenice = Listbox(okvir,
                   font=mojFont,
                   width=25,
                   height=5,
                   bg='#cacdd6',  # Boja pozadine
                   bd=0,  # Border
                   fg='#402a32',
                   highlightthickness=0,  # Obrub kada se klikne
                   selectbackground='#e5c1cd',
                   activestyle='none'
                   )
lubenice.pack(side=LEFT, fill=BOTH)
lista = []
for zadaci in lista:
    lubenice.insert(END, zadaci)

# Stvaranje scrollbara
scroll = Scrollbar(okvir)
scroll.pack(side=RIGHT, fill=BOTH)

# Dodavanje scrollbara listi zadataka
lubenice.config(yscrollcommand=scroll.set)
scroll.config(command=lubenice.yview)

# Prozor za unos
unos = Entry(luby, font=mojFont, bg='#cacdd6')
unos.pack(pady=20)

# Okvir za gumbe
button_okvir = Frame(luby)
button_okvir.pack(pady=20)


# Funkcije za rukovanje zadacima
# Funkcija za prikaz poruke ako nema zadatka
def nema_zadatka():
    mb.showinfo('Info', 'Nema dostupnih zadataka za brisanje')
    return


def sigurno_brisi():
    if not lubenice.curselection(): #nije označen niti jedan zadatak
        mb.showinfo('Info', 'Niste odabrali niti jedan zadatak')
        return
    odgovor = mb.askyesnocancel('Potvrdi brisanje', 'Jeste li sigurni da želite \nizbrisati odabrani zadatak?')
    if odgovor is None:
        return
    elif odgovor:
        if lubenice.size() == 0:
            nema_zadatka()
        else:
            lubenice.delete(ANCHOR)
    return


def dodaj_zadatak(event=None):  # Accept event as an argument
    novi_zadatak = unos.get()
    if novi_zadatak.strip() == "":
        mb.showwarning("Upozorenje", "Zadatak ne može biti prazan.")
        return

    # Provjera postoji li već zadatak s istim imenom
    for i in range(lubenice.size()):
        if lubenice.get(i) == novi_zadatak:
            mb.showwarning("Upozorenje", "Zadatak s istim imenom već postoji.")
            return

    lubenice.insert(END, novi_zadatak)
    unos.delete(0, END)

def rijesi_zadatak():
    if not lubenice.curselection(): #nije označen niti jedan zadatak
        mb.showinfo('Info', 'Niste odabrali niti jedan zadatak')
    else:
        lubenice.itemconfig(lubenice.curselection(), fg='#9d8cb1')
        lubenice.selection_clear(0, END)

def vrati_zadatak():
    if not lubenice.curselection(): #nije označen niti jedan zadatak
        mb.showinfo('Info', 'Niste odabrali niti jedan zadatak')
    else:
        lubenice.itemconfig(lubenice.curselection(), fg='#402a32')
        lubenice.selection_clear(0, END)

def brisi_rijesene():
    if lubenice.size() == 0:
        nema_zadatka()
    else:
        brojac = 0
        while brojac < lubenice.size():
            if lubenice.itemcget(brojac, 'fg') == '#9d8cb1':
                lubenice.delete(brojac)
            else:
                brojac += 1

# Dodavanje gumba
brisi = Button(button_okvir, text='Obriši zadatak', command=sigurno_brisi, bg='#c48b86')
dodaj = Button(button_okvir, text='Dodaj zadatak', command=dodaj_zadatak, bg='#c48b86')
rijesi = Button(button_okvir, text='Riješi zadatak', command=rijesi_zadatak, bg='#c48b86')
vrati = Button(button_okvir, text='Vrati zadatak', command=vrati_zadatak, bg='#c48b86')
brisi_rijesene = Button(button_okvir, text='Izbriši riješene', command=brisi_rijesene, bg='#c48b86')

brisi.grid(row=0, column=0)
dodaj.grid(row=0, column=1)
rijesi.grid(row=0, column=2)
vrati.grid(row=0, column=3)
brisi_rijesene.grid(row=0, column=4)

# Luby timer POSTAVKE
luby_running = False
luby_seconds = 25 * 60  # 25 minuta
#luby_seconds = 0.25 * 60 

def start_timer():
    global luby_running
    if not luby_running:
        luby_running = True
        count_down()

def pause_timer():
    global luby_running
    luby_running = False

def reset_timer():
    global luby_running, luby_seconds
    luby_running = False
    luby_seconds = 25 * 60
    timer_label.config(text="25:00")

def count_down():
    global luby_seconds
    if luby_running and luby_seconds >= 0:
        minutes, seconds = divmod(luby_seconds, 60)
        timer_label.config(text=f"{minutes:02}:{seconds:02}")
        luby_seconds -= 1
        luby.after(1000, count_down)
    elif luby_seconds <= 0:
        mb.showinfo("Vrijeme je isteklo", "Vrijeme je za pauzu!")
        mb.showinfo('Vrijeme je isteklo', 'Nemoj zaboraviti popiti vode i rastegnuti se!')
        reset_timer()

# Okvir za Luby timer
luby_frame = Frame(luby, bg='#a8aab2')
luby_frame.pack(pady=20)

timer_label = Label(luby_frame, text="25:00", font=("Maiandra GD", 48), bg='#a8aab2')
timer_label.pack(pady=10)

zapocni = Button(luby_frame, text="Započni", command=start_timer, bg='#c48b86')
pauziraj = Button(luby_frame, text="Pauziraj", command=pause_timer, bg='#c48b86')
resetiraj = Button(luby_frame, text="Resetiraj", command=reset_timer, bg='#c48b86')

zapocni.pack(side=LEFT, padx=5)
pauziraj.pack(side=LEFT, padx=5)
resetiraj.pack(side=LEFT, padx=5)

# Povezivanje funkcije sa enterom
luby.bind('<Return>', dodaj_zadatak)

luby.mainloop()
