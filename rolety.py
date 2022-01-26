import random
import tkinter

window = tkinter.Tk()
canvas = tkinter.Canvas(window, width=900, heigh=650)
canvas.pack()


class windowScenery:
    """
        Trieda, ktorá drží celú hru.
        Obsahuje funkcie: __init__, rebuild, move_shade, set_control_shade, bindings
    """
    # Premenné slúžiace na ovládanie hry
    shades = []
    shade_move = False
    control_shade = 0
    control_direction = "Up"

    def __init__(self, master, input_number_of_shades):
        """
            Konštruktor triedy, ktorý nám ju automaticky zostaví.
            :param master: inštancia tkinter.Tk()
            :type master: tkinter.Tk()
            :param input_number_of_shades: Označuje počet roliet, ktoré má zostaviť na obrazovke.
            :type input_number_of_shades: int
        """
        # Zapisovanie premenných, ktoré prišli ako parameter
        self.master = master
        self.number_of_shades = input_number_of_shades
    
        # Nastavovanie rozlíšenia, pozadia a pridávanie tlačítka a poľa na písanie
        canvas.configure(background = "lightblue", width = self.number_of_shades * 300)
        self.entry = tkinter.Entry(master)
        self.entry.pack()
        self.button = tkinter.Button(master, text="Zmeň počet roliet!", command = self.rebuild)
        self.button.pack()

        # Generovanie krajiny
        coordinates = {
            "x1": -50,
            "y1": 325,
            "x2": 0,
            "y2": 0
        }
        for i in range(self.number_of_shades):
            width = random.randint(( 300 * (i + 1) ) - coordinates["x1"] + 100, ( 300 * (i + 1) ) - coordinates["x1"] + 300)
            height = random.randint(650 - coordinates["y1"] + 300, 650 - coordinates["y1"] + 400)

            coordinates["x2"] = coordinates["x1"] + width
            coordinates["y2"] = coordinates["y1"] + height

            canvas.create_oval(coordinates["x1"], coordinates["y1"], coordinates["x2"], coordinates["y2"], fill = "green", outline = "green")

            coordinates["x1"] = coordinates["x2"] - random.randint(0,250)
            coordinates["y1"] = 325 + random.randint(-100, 100)
            coordinates["x2"] = 0
            coordinates["y2"] = 0

        # Generovanie čiar, ktoré oddeľujú jednotlivé rolety
        for i in range(0, self.number_of_shades + 1):
            canvas.create_line(i * 300, 0, i*300, 650, fill = "black", width = 10)

        # Generovanie samotných roliet
        for i in range(self.number_of_shades):
            self.shades.append([])
            for j in range(int(650 / 10)):
                self.shades[i].append(canvas.create_rectangle(i * 300 + 5, j * 10, i * 300 - 5 + 300, j * 10 + 10, fill = "brown", outline = "black"))

        # Volanie funkcií na nabindovanie stláčania tláčidiel
        self.bindings()
        # Nastavovanie stavu hry, že je pripravená na hranie
        self.init_status = True

    def rebuild(self):
        """
            Funkcia, ktorá je volaná na prenastavenie počtu roliet hry t.j. jej pregenerovanie.
        """
        new_number_of_shades = int(self.entry.get())
        if new_number_of_shades >= 1:  
            # Mazanie všetkého obsahu z plátna      
            canvas.delete("all")
            self.entry.destroy()
            self.button.destroy()

            # Tvorenie nového objektu hry
            self = windowScenery(self.master, new_number_of_shades)
        else:
            print("Okno musí mať minimálne jednu roletu.")

    def move_shade(self, direction):
        """
            Funkcia, ktorá slúži na celkové ovládanie roliet.
            :param direction: Označuje smer ovládania.
            :type direction: string
        """
        if self.shade_move == True:
            # Zastavovanie pohybu rolety
            print(f"Stopping shade {self.control_shade} with direction {self.control_direction}")
            self.shade_move = False
            self.control_direction = direction
        else:
            self.shade_move = True
            self.control_direction = direction
            print(f"Moving shade {self.control_shade} with direction {self.control_direction}")

            if self.control_direction == "Up":
                # Pohyb rolety smerom nahor
                while len(self.shades[self.control_shade]) and self.shade_move:
                    if self.shades[self.control_shade][-1] == None:
                        break
                        
                    canvas.delete(self.shades[self.control_shade][-1])
                    del self.shades[self.control_shade][-1]
                    canvas.update()
                    canvas.after(100)
                self.shade_move = False
            elif self.control_direction == "Down":
                # Pohyb rolety smerom nadol
                if self.shades[self.control_shade] and list(canvas.bbox(self.shades[self.control_shade][-1]))[3] == 651:
                    # Ošetrenie špeciálneho prípadu v možnosti, že roleta je zatiahnutá a stláčame tlačidlo nadol    
                    for i in range(len(self.shades[self.control_shade])):
                        if not self.shade_move:
                            break

                        if self.shades[self.control_shade][i] != None:
                            canvas.delete(self.shades[self.control_shade][i])
                            del self.shades[self.control_shade][i]

                            self.shades[self.control_shade].insert(i, None)

                            canvas.update()
                            canvas.after(100)
                    self.shade_move = False                        
                else:
                    # Klasický pohyb rolety smerom nadol ku koncu
                    while len(self.shades[self.control_shade]) < 65 and self.shade_move:
                        n = len(self.shades[self.control_shade])
                        self.shades[self.control_shade].append(canvas.create_rectangle((self.control_shade) * 300 + 5, n * 10, (self.control_shade) * 300 + 300 - 5, n * 10 + 10, fill = "brown", outline = "black"))
                        canvas.update()
                        canvas.after(100)
                    self.shade_move = False
            else:
                print("Invalid direction of move.")

    def set_control_shade(self, new_control_shade, r_l_control = False):
        """
            Funkcia, ktorá slúži na prepínanie aktuálne ovládanej rolety.
            :param new_control_shade: Označuje index rolety, ktorú chceme aktuálne ovládať.
            :type new_control_shade: int
            :param r_l_control: Slúži na odlíšenie ovládania šípkami, pri počte roliet inom ako 3. Základný stav je False.
            :type r_l_control: boolean
        """
        if r_l_control and self.number_of_shades != 3:
            # Ovládanie šípkami vpravo vľavo
            print(f"Chaning control from {self.control_shade} to next one on the {new_control_shade}.")
            if new_control_shade == "Right":
                if self.control_shade == self.number_of_shades - 1:
                    self.control_shade = 0
                else:
                    self.control_shade += 1
            if new_control_shade == "Left":
                if self.control_shade == 0:
                    self.control_shade = self.number_of_shades - 1
                else:
                    self.control_shade -= 1
            print(f"Now controlling {self.control_shade}")
        elif not r_l_control and self.number_of_shades == 3:
            # Ovládanie pomocou stláčania tlačidiel na numerickej klávesnici
            print(f"Changing control from {self.control_shade} to {new_control_shade}")
            self.control_shade = int(new_control_shade)

    def bindings(self):
        """
            Funkcia, ktorá po zavolaní nabinduje všetky tlačítka potrebné pre ovládanie hry.
        """
        # Escape - pre ukončenie hry
        self.master.bind("<Escape>", lambda _: self.master.destroy())

        # Up, Down - pre ovládanie pohybu roliet
        for dir in ["Up", "Down"]:
            self.master.bind(f"<{dir}>", lambda event: self.move_shade(event.keysym))

        # Right, Left - pre ovládanie aktívnej rolety v prípade, že počet roliet je iný ako 3
        for dir in ["Right", "Left"]:
            self.master.bind(f"<{dir}>", lambda event: self.set_control_shade(event.keysym, True))

        # Nabindovanie tlačidiel numerickej klávesnice od 1 po 9 pre ovládanie aktívnej rolety v prípade, že počet roliet je 3
        for i in range(1, 10): 
            self.master.bind(str(i), lambda event: self.set_control_shade(str(int(event.keysym) - 1)))

# Automatické vytváranie objektu hry pri jej spustení
windowScene = windowScenery(window, 3)
window.mainloop()

