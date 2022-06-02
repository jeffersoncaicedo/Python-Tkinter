import tkinter as tk
import sqlite3

from tkinter import *
from tkinter import ttk, messagebox
from tkinter.ttk import Treeview



def llenado():
    lblpres.config(text="Empieza el ciclo de llenado")
    conectar = sqlite3.connect('DBCaudal.db')
    cur = conectar.cursor()
    for i in range(6):
        fnew = input("Agregar Fecha: ")
        hnew = input("Agregar Hora: ")
        cnew = input("Agregar el valor del caudal: ")
        datos = [(fnew, hnew, cnew)]
        cur.executemany('''INSERT INTO caudal 
                        VALUES (null, ?, ?, ?)''', datos)
        conectar.commit()
        cur.execute('''SELECT COUNT(*) FROM caudal''')
        n = cur.fetchall()
        tabla.insert("", tk.END, text=(n[0][0]), values=(fnew, hnew, cnew))
    conectar.close()
    lblpres.config(text="Ciclo de llenado terminado")
    

def consulta():
    texto.set("dd/mm/aaaa")
    fecha.bind("<FocusIn>", borrar)
    fecha.bind("<FocusOut>", borrar)
    princ.pack_forget()
    sec.pack(side='top', fill='both', expand=True)


def borrar(event):
    texto.set("")


def inicio():
    root.focus()
    sec.pack_forget()
    princ.pack(side='top', fill='both', expand=True)
    lblpres.config(text="Bienvenido a la ventana principal")

def info():
    root.focus()
    conectar = sqlite3.connect('DBCaudal.db')
    cur = conectar.cursor()
    cur.execute('''SELECT EXISTS(SELECT Fecha FROM caudal WHERE Fecha = '%s')''' %fecha.get())
    a = cur.fetchall()
    cur.execute('''SELECT avg(Caudal) FROM caudal WHERE Fecha = '%s' ''' %fecha.get())
    b = cur.fetchall()
    conectar.close()
    if a[0][0]:
       messagebox.showinfo("Promedio", "El promedio de caudal de la fecha %s es: %.2f" %(fecha.get(), b[0][0]))
    else:
        messagebox.showerror("Error", "La fecha solicitada no existe en el registro")

def validarentrada(new_text):
    if len(new_text) > 10:
        return False
    cheq = []
    for i, char in enumerate(new_text):
        if i in (2, 5):
            cheq.append(char == "/")
        else:
            cheq.append(char.isdecimal())
    return all(cheq)

#Área de Trabajo
root = tk.Tk()
root.title("Python-Tkinter")
root.geometry('800x480')

#Ventana Principal
princ = tk.Frame(root)
princ.pack(side='top', fill='both', expand=True)
princ.config(bg='#8bdcf0')

#Ventana Secundaria
sec = tk.Frame(root)

#Widgets de la Ventana Principal
lblpres = Label(princ, text="Bienvenido a la ventana principal", bg='#8bdcf0', font=32)
lblpres.pack(padx=200, pady=80, ipadx=200, ipady=20)
btnciclo = Button(princ, text="Ciclo de Llenado", command=llenado, font=24, bg='#f99577')
btnciclo.place(x=150, y=280, width=150, height=30)
btncons = Button(princ, text="Mostrar datos", command=consulta, font=24, bg='#f99577')
btncons.place(x=500, y=280, width=150, height=30)

#Widgets de la Ventana Secundaria
texto = StringVar()
texto.set("dd/mm/aaaa")
fecha = ttk.Entry(sec, justify=tk.CENTER, textvariable=texto, validate="key", 
                    validatecommand=(sec.register(validarentrada), "%P"))
fecha.place(x=600, y=160, width=195, height=25)
fecha.bind("<FocusIn>", borrar)
fecha.bind("<FocusOut>", borrar)
btnconsulta = Button(sec, text="Consultar Promedio", command=info)
btnconsulta.place(x=620, y=210, width=150, height=30)
btninicio = Button(sec, text="Inicio", command=inicio)
btninicio.place(x=650, y=260, width=100, height=30)
tabla = Treeview(sec, columns=('1', '2', '3'))
tabla.heading('#0', text="N°")
tabla.heading('1', text="Fecha")
tabla.heading('2', text="Hora")
tabla.heading('3', text="Caudal (m{}/s)".format(chr(0xB3)))
#tabla.heading('4', text="Promedio(m{}/s)".format(chr(0xB3)))
tabla.column('#0', width=40, anchor='center')
tabla.column('1', width=185, anchor='center')
tabla.column('2', width=185, anchor='center')
tabla.column('3', width=185, anchor='center')
#tabla.column('4', width=140, anchor='center')
tabla.place(x=0, y=0, width=600, height=480)

#Manejo de la Base de Datos
conectar = sqlite3.connect('DBCaudal.db')
cur = conectar.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS caudal
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                Fecha DATE NOT NULL,
                Hora TIME NOT NULL,
                Caudal FLOAT NOT NULL)''')
cur.execute('''SELECT COUNT(*) FROM caudal''')
er = cur.fetchall()
if er[0][0] > 0:
    cur.execute("SELECT id FROM caudal")
    ide = cur.fetchall()
    cur.execute('''SELECT Fecha, Hora, Caudal FROM caudal''')
    tabladatos = cur.fetchall()
    for i in range(er[0][0]):
        tabla.insert("", tk.END, text=ide[i][0], values=(tabladatos[i][0], tabladatos[i][1], tabladatos[i][2]))
conectar.close()

#Creación de la ventana
root.mainloop()