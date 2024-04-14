import tkinter as tk
from tkinter import messagebox
import random

class RegistroJugador:
    def __init__(self, master, callback):
        self.master = master
        self.callback = callback

        self.master.title("Registro de Jugador")
        self.master.geometry("800x600")

        self.label_nombre = tk.Label(self.master, text="Nombre de jugador:", font=("Arial", 16))
        self.label_nombre.pack(pady=20)

        self.entry_nombre = tk.Entry(self.master, font=("Arial", 14))
        self.entry_nombre.pack(pady=20)

        self.btn_registrar = tk.Button(self.master, text="Registrar", command=self.registrar_jugador, font=("Arial", 14))
        self.btn_registrar.pack()

    def registrar_jugador(self):
        nombre = self.entry_nombre.get()
        if nombre.strip():
            self.master.withdraw()
            self.callback(nombre)
        else:
            messagebox.showwarning("Advertencia", "Ingresa un nombre de jugador válido.")

class JuegoAhorcado:
    def __init__(self, master, nombre_jugador):
        self.master = master
        self.master.title("Juego del Ahorcado")
        self.master.geometry("800x600")

        self.nombre_jugador = nombre_jugador
        self.iniciar_juego()

    def iniciar_juego(self):
        self.palabra_secreta = self.seleccionar_palabra()
        self.letras_adivinadas = []
        self.intentos_maximos = 10
        self.intentos = 0

        self.lbl_palabra = tk.Label(self.master, text=self.mostrar_tablero(), font=("Arial", 16))
        self.lbl_palabra.pack(pady=20)

        self.lbl_intentos = tk.Label(self.master, text=f"Intentos restantes: {self.intentos_maximos}", font=("Arial", 12))
        self.lbl_intentos.pack()

        self.entry_letra = tk.Entry(self.master, font=("Arial", 14))
        self.entry_letra.pack(pady=10)

        self.btn_adivinar = tk.Button(self.master, text="Adivinar", command=self.verificar_letra, font=("Arial", 14))
        self.btn_adivinar.pack()

        self.canvas = tk.Canvas(self.master, width=200, height=200)
        self.canvas.pack()
        self.dibujar_ahorcado()

    def seleccionar_palabra(self):
        palabras = ["python", "programacion", "ahorcado", "juego", "computadora", "inteligencia"]
        return random.choice(palabras)

    def mostrar_tablero(self):
        tablero = ""
        for letra in self.palabra_secreta:
            if letra in self.letras_adivinadas:
                tablero += letra + " "
            else:
                tablero += "_ "
        return tablero.strip()

    def verificar_letra(self):
        letra = self.entry_letra.get().lower()

        if letra.isalpha() and len(letra) == 1:
            if letra in self.letras_adivinadas:
                messagebox.showinfo("Aviso", "Ya has adivinado esa letra. ¡Inténtalo de nuevo!")
            elif letra in self.palabra_secreta:
                self.letras_adivinadas.append(letra)
                self.actualizar_tablero()
            else:
                self.intentos += 1
                self.lbl_intentos.config(text=f"Intentos restantes: {self.intentos_maximos - self.intentos}")
                self.dibujar_ahorcado()
                if self.intentos == self.intentos_maximos:
                    self.mostrar_fin_juego("Perdiste. La palabra era: " + self.palabra_secreta)
        else:
            messagebox.showwarning("Advertencia", "Ingresa una letra válida.")

    def actualizar_tablero(self):
        self.lbl_palabra.config(text=self.mostrar_tablero())
        if "_" not in self.mostrar_tablero():
            self.mostrar_fin_juego("¡Felicidades, {}! Has adivinado la palabra: {}".format(self.nombre_jugador, self.palabra_secreta))

    def mostrar_fin_juego(self, mensaje):
        resultado = messagebox.askquestion("Fin del juego", mensaje + "\n¿Quieres jugar de nuevo?")
        if resultado == "yes":
            self.reiniciar_juego()
        else:
            self.master.destroy()

    def reiniciar_juego(self):
        if hasattr(self, 'lbl_palabra') and self.lbl_palabra.winfo_exists():
            self.lbl_palabra.destroy()

        if hasattr(self, 'lbl_intentos') and self.lbl_intentos.winfo_exists():
            self.lbl_intentos.destroy()

        if hasattr(self, 'entry_letra') and self.entry_letra.winfo_exists():
            self.entry_letra.destroy()

        if hasattr(self, 'btn_adivinar') and self.btn_adivinar.winfo_exists():
            self.btn_adivinar.destroy()

        if hasattr(self, 'canvas') and self.canvas.winfo_exists():
            self.canvas.destroy()

        self.iniciar_juego()

    def dibujar_ahorcado(self):
        partes_ahorcado = [
            (50, 190, 150, 190),  # Base horizontal
            (100, 190, 100, 50),  # Poste vertical
            (100, 50, 150, 50),   # Cuerda
            (150, 50, 150, 80),   # Cabeza
            (140, 80, 160, 80),   # Cuello
            (150, 80, 150, 120),  # Cuerpo
            (150, 95, 130, 115),  # Brazo izquierdo
            (150, 95, 170, 115),  # Brazo derecho
            (150, 120, 130, 140),  # Pierna izquierda
            (150, 120, 170, 140),  # Pierna derecha
        ]

        if self.intentos > 0 and self.intentos <= len(partes_ahorcado):
            parte = partes_ahorcado[self.intentos - 1]
            self.canvas.create_line(parte, width=3)
        if self.intentos == self.intentos_maximos:
            self.mostrar_fin_juego("Perdiste. La palabra era: " + self.palabra_secreta)

def main():
    root = tk.Tk()

    def iniciar_juego_con_registro(nombre_jugador):
        registro_window.withdraw()
        juego_ahorcado = JuegoAhorcado(root, nombre_jugador)

    registro_window = tk.Toplevel(root)
    registro_window.title("Registro de Jugador")
    registro_window.geometry("800x600")

    registro = RegistroJugador(registro_window, iniciar_juego_con_registro)

    root.mainloop()

if __name__ == "__main__":
    main()
