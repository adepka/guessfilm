import tkinter as tk
import random

atbildes = []
pogas=[]
tema = ""
jautajumBildes=[]
nosaukums = []
filmaBildes= []
seciba=[]

#-------------------- datu sagatavošana -----------------------#
# nolasa jautājumu banku
def funkDATI():
    jaut_bildes = []
    atb_bildes = []
    atb_teksts = []
    f = open("banka.txt", "r", encoding = "utf-8")  
    nr = 0

    tema = "Uzmini filmiņu" # Nosaukums pec noklusejuma

    for rinda in f:
        rindaTeksts = rinda.strip()

        if nr == 0 and rindaTeksts.count("|") != 2: 
            tema = rindaTeksts
        elif rindaTeksts.count("|") == 2:
            parts = rindaTeksts.split("|")
            jaut_bildes.append(parts[0])
            atb_teksts.append(parts[1])
            atb_bildes.append(parts[2])
        nr += 1
    f.close()

    return tema, jaut_bildes, atb_teksts, atb_bildes

def funkSajaukt():
    seciba = []
    # izveido nejaušu kārtas numuru secību
    for i in range(len(jautajumBildes)):
        seciba.append(i)
    random.shuffle(seciba)
    jaut = []
    atb_b = []
    atb_t = []
    for i in range(10):
        jaut.append(jautajumBildes[seciba[i]])
        atb_b.append(filmaBildes[seciba[i]])
        atb_t.append(nosaukums[seciba[i]])
    return jaut, atb_t, atb_b

def funkSAKT():
    global atbildes, jautajumBildes, filmaBildes, nosaukums, tema

    if len(atbildes) == 10:
        atbildes=[]
        beiga_skats.pack_forget() 

    #---- Miksejam jautajumus ----#
    jautajumBildes, nosaukums, filmaBildes = funkSajaukt()    
    
    logs.attributes('-fullscreen', True)
    # aizver sākuma skatu un atver režģa skatu
    sakuma_skats.pack_forget()  
    funkIzvelesEkrans()

def funkIzvelesEkrans():
    rezga_skats.pack(fill = 'both', expand = True)  

def funkJAUTAJUMS(izvele):
    rezga_skats.pack_forget()  
    
    global tekosais_jautajums
    tekosais_jautajums = izvele

    atbildes.append(izvele)

    bildes_cels = "bildes/" + jautajumBildes[(tekosais_jautajums - 1)]  # bildes url
    j_bilde = tk.PhotoImage(file=bildes_cels)
    
    jautajuma_attels.config(image=j_bilde)
    jautajuma_attels.image = j_bilde    
    
    jautajuma_skats.pack(fill = 'both', expand = True)  

def funkREZULTATS():
    jautajuma_skats.pack_forget() 

    filma_nosaukums = nosaukums[(tekosais_jautajums - 1)]  # Nosaukums
    bildes_cels = "bildes/" + filmaBildes[(tekosais_jautajums - 1)]  # bildes url
    a_bilde = tk.PhotoImage(file=bildes_cels)

    rezultata_uzraksts.config(text=filma_nosaukums)

    rezultata_attels.config(image=a_bilde)
    rezultata_attels.image = a_bilde    

    rezultata_skats.pack(fill = 'both', expand = True)  

def funkTalak():
    global atbildes

    #- Fiksejam atbildi pie režģa
    pogas_krasa = "#F1C68E"
    pogas_status = "disabled"
    
    if len(atbildes) == 10:
        pogas_krasa = "#FFFFFF"
        pogas_status = "normal"
        
    for nr in atbildes:
        pogas[nr - 1].config(
            state=pogas_status,
            bg=pogas_krasa,
        )

    rezultata_skats.pack_forget()
    if len(atbildes) == 10:
        beiga_skats.pack(fill = 'both', expand = True)  
    else:
        funkIzvelesEkrans()
def close_all_windows():
    logs.destroy()

#---- Lasam datus no banka ----#
tema, jautajumBildes, nosaukums, filmaBildes = funkDATI()

#--- Sakam konstruet interfeicu
#--- gatavojam galveno ekranu ---#
logs = tk.Tk()
logs.title("Konkurss")
platums = logs.winfo_screenwidth()
augstums = logs.winfo_screenheight()
logs.resizable(False, False) 
logs.geometry(f"{platums}x{augstums}+{-10}+{0}")
logs.configure(bg = '#EEEEEE')

#------------------------------ sākuma skats -----------------------------#
sakuma_skats = tk.Frame(logs)
# uzraksts
uzraksts = tk.Label(sakuma_skats, text=tema, fg = '#800000', font=('Verdana', 24, 'bold'))
uzraksts.pack(pady = augstums // 10)
# ielādē attēlu
image = tk.PhotoImage(file = "bildes\puzzle.png")  
# izveido Label, lai parādītu attēlu
attels = tk.Label(sakuma_skats, image = image)
attels.pack(pady = 10)
# izveido pogu
poga = tk.Button(sakuma_skats, text = "Sākt", command = funkSAKT, 
                 width = 20, height=2, bg = 'lightgrey', 
                 fg = '#800000', font = ('Verdana', 12, 'bold'))
poga.pack(pady = augstums // 20)

#---------------------------- režģa skats ----------------------------#
rezga_skats = tk.Frame(logs)

# izveido Label
rezgid_uzraksts = tk.Label(rezga_skats, text="Izvēlieties numuru no tabulas!", fg = '#800000', font=('Verdana', 24, 'bold'))
rezgid_uzraksts.pack(pady = augstums // 10)

# Centretā pozicija ar ievietotu freimu
centrs = tk.Frame(rezga_skats)
centrs.place(relx=0.5, rely=0.5, anchor='center')

# Pogas izmers
pogas_platums = platums // 15
pogas_augstums = augstums // 15

for i in range(1, 11):
    #-- funkcijas izsaukums or GPT palidzibu --#
    poga = tk.Button(centrs, text=str(i), font=('Verdana', 34, 'bold'), width=5, height=2, command=lambda x=i: funkJAUTAJUMS(x))
    poga.grid(row=(i-1)//5, column=(i-1)%5, padx=pogas_platums // 10, pady=pogas_augstums // 10)  # 2 rindas ar 5 pogiem
    pogas.append(poga)

#------------------------------ jautajuma skats -----------------------------#
jautajuma_skats = tk.Frame(logs)
# izveido Label, lai parādītu jautajumu
jaut_uzraksts = tk.Label(jautajuma_skats, text="Kas par filmu?", fg = '#800000', font=('Verdana', 24, 'bold'))
jaut_uzraksts.pack(pady = augstums // 20)
# ielādē attēlu
jautajuma_image = tk.PhotoImage(file = "bildes\puzzle.png")  
jautajuma_attels = tk.Label(jautajuma_skats, image = image)
jautajuma_attels.pack(pady = 0)
# izveido pogu
pogaAtbilde = tk.Button(jautajuma_skats, text = "Atbilde", command = funkREZULTATS, 
                 width = 20, height=2, bg = 'lightgrey', 
                 fg = '#800000', font = ('Verdana', 12, 'bold'))
pogaAtbilde.pack(pady = augstums // 20)
#------------------------------ rezultata skats -----------------------------#
rezultata_skats = tk.Frame(logs)
# izveido Label, lai parādītu nosaukumu
rezultata_uzraksts = tk.Label(rezultata_skats, text="", fg = '#800000', font=('Verdana', 24, 'bold'))
rezultata_uzraksts.pack(pady = augstums // 20)
# ielādē attēlu
rezultata_image = tk.PhotoImage(file = "bildes\puzzle.png")  
rezultata_attels = tk.Label(rezultata_skats, image = image)
rezultata_attels.pack(pady = 0)
# izveido pogu
pogaTalak = tk.Button(rezultata_skats, text = "Talak", command = funkTalak, 
                 width = 20, height=2, bg = 'lightgrey', 
                 fg = '#800000', font = ('Verdana', 12, 'bold'))
pogaTalak.pack(pady = augstums // 20)
#------------------------------ Beiga skats -----------------------------#
beiga_skats = tk.Frame(logs)

# uzraksts
beiga_uzraksts = tk.Label(beiga_skats, text="Well Done!", fg = '#800000', font=('Verdana', 24, 'bold'))
beiga_uzraksts.pack(pady = augstums // 10)
# ielādē attēlu
beiga_image = tk.PhotoImage(file = "bildes/welldone.png")  
# izveido Label, lai parādītu attēlu
beiga_attels = tk.Label(beiga_skats, image = beiga_image)
beiga_attels.pack(pady = 10)
# izveido pogas
beiga_poga = tk.Button(beiga_skats, text = "Sākt no jauna", command = funkSAKT, 
                 width = 20, height=2, bg = 'lightgrey', 
                 fg = '#800000', font = ('Verdana', 12, 'bold'))
beiga_poga.pack(pady = augstums // 10)
beiga_poga_beigt = tk.Button(beiga_skats, text = "Beigt", command = close_all_windows, 
                 width = 20, height=2, bg = '#000000', 
                 fg = '#FFFFFF', font = ('Verdana', 12, 'bold'))
beiga_poga_beigt.pack(pady = 5)


sakuma_skats.pack(fill = 'both', expand = True)
logs.mainloop()