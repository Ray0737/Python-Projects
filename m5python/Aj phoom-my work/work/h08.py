import tkinter as tk
from tkinter import ttk
from scipy.constants import kilo, mega, giga, tera, peta, exa, zetta, yotta, hecto, deka, deci
from scipy.constants import milli, micro, nano, pico, femto, atto, zepto, centi
from scipy.constants import zero_Celsius, degree_Fahrenheit
from scipy.constants import kibi, mebi, gibi, tebi, pebi, exbi, zebi, yobi
from scipy.constants import electron_volt, calorie, calorie_IT, erg, Btu, Btu_th, ton_TNT
from scipy.constants import dyn, dyne, lbf, pound_force, kgf, kilogram_force

def convert_units(category):
    value_str = entry_value.get()

    if not value_str.replace('.', '', 1).isdigit():
        result_label.config(text="Please enter a valid value.")
        return

    number = float(value_str)
    from_unit = combo_1.get()
    to_unit = combo_2.get()

    if category == 'Temperature':
        if from_unit == 'Celsius' and to_unit == 'Fahrenheit':
            result = (number * 9/5) + 32
        elif from_unit == 'Fahrenheit' and to_unit == 'Celsius':
            result = (number - 32) * 5/9
        elif from_unit == 'Celsius' and to_unit == 'Kelvin':
            result = number + 273.15
        elif from_unit == 'Kelvin' and to_unit == 'Celsius':
            result = number - 273.15
        elif from_unit == 'Fahrenheit' and to_unit == 'Kelvin':
            result = (number - 32) * 5/9 + 273.15
        elif from_unit == 'Kelvin' and to_unit == 'Fahrenheit':
            result = (number - 273.15) * 9/5 + 32
        else:
            result_label.config(text="Incorrect unit selection.")
            return
    else:
        if from_unit in all_units[category] and to_unit in all_units[category]:
            conversion_rate = all_units[category][from_unit] / all_units[category][to_unit]
            result = number * conversion_rate
        else:
            result_label.config(text="Incorrect unit selection.")
            return

    result_label.config(text=f'{result:.4f} {to_unit}')

def con_window(category, units):
    global combo_1, combo_2, result_label, entry_value, root2
    root.withdraw()
    root2 = tk.Tk()
    root2.title(category)
    root2.option_add('*font', 'Terminal 17')
    root2.geometry('350x480')
    
    tk.Label(root2, text=f'การแปลง {category}', fg='palevioletred3', width=34).place(x=0,y=0)
    tk.Label(root2, text='from :').place(x=20,y=50)
    
    entry_value = tk.Entry(root2)
    entry_value.place(x=100, y=50)
    
    combo_1 = ttk.Combobox(root2, values=units)
    combo_1.place(x=100, y=85)
    
    tk.Label(root2, text='    to :').place(x=0, y=150)
    
    combo_2 = ttk.Combobox(root2, values=units)
    combo_2.place(x=100, y=150)
    
    button_submit = tk.Button(root2, text='SUBMIT', fg='white', bg='pink2', font='bold', command=lambda: convert_units(category))
    button_submit.place(x=100, y=200)
    
    tk.Label(root2, text='result :').place(x=8, y=280)
    
    result_label = ttk.Label(root2, text=" ", font=('Terminal', 12))
    result_label.place(x=100, y=286)
    
    button_undo = tk.Button(root2, text='BACK', fg='white', bg='pink2', font='bold', command=undo)
    button_undo.place(x=100, y=330)
    
    root2.mainloop()

def undo():
    root2.destroy()
    root.deiconify()

def metric():
    con_window('Metric Prefixes', list(all_units['Metric Prefixes'].keys()))

def mass():
    con_window('Mass', list(all_units['Mass'].keys()))

def temperature():
    con_window('Temperature', list(all_units['Temperature'].keys()))

def energy():
    con_window('Energy', list(all_units['Energy'].keys()))

def force():
    con_window('Force', list(all_units['Force'].keys()))

all_units = {
    'Metric Prefixes': {
        'yotta': yotta, 'zetta': zetta, 'exa': exa, 'peta': peta, 'tera': tera, 'giga': giga, 'mega': mega,
        'kilo': kilo, 'hecto': hecto, 'deka': deka, 'deci': deci,'meter': 1,'centi': centi, 'milli': milli,
        'micro': micro, 'nano': nano, 'pico': pico, 'femto': femto, 'atto': atto, 'zepto': zepto,
    },
    'Mass': {
        'kibi': kibi, 'mebi': mebi, 'gibi': gibi, 'tebi': tebi, 'pebi': pebi, 'exbi': exbi, 'zebi': zebi, 'yobi': yobi
    },
    'Temperature': {
        'Celsius': zero_Celsius, 'Fahrenheit': degree_Fahrenheit, 'Kelvin': 1 
    },
    'Energy': {
        'electron_volt': electron_volt, 'calorie': calorie, 'calorie_IT': calorie_IT, 'erg': erg,
        'Btu': Btu, 'Btu_th': Btu_th, 'ton_TNT': ton_TNT
    },
    'Force': {
        'dyn': dyn, 'dyne': dyne, 'lbf': lbf, 'pound_force': pound_force, 'kgf': kgf, 'kilogram_force': kilogram_force
    }
}

root = tk.Tk()
root.title('Unit Converter')
root.option_add('*font', 'Terminal 16')
root.geometry('340x485')

topic = tk.Label(root, text='convert unit', bg='pink2')
topic.pack(fill=tk.X)

guide = tk.Label(root, text='please select unit', bg='white')
guide.pack(fill=tk.X)

button_metric = tk.Button(text='SI', compound=tk.TOP, fg='white', bg='pink2', relief='ridge', font=50,  command=metric)
button_metric.place(x=115,y=90,height=50,width=120)

button_mass = tk.Button(text='Mass', compound=tk.TOP, fg='white', bg='pink2', relief='ridge', font=50, command=mass)
button_mass.place(x=115,y=165,height=50,width=120)

button_energy = tk.Button(text='Energy', compound=tk.TOP, fg='white', bg='pink2', relief='ridge', font=50, command=energy)
button_energy.place(x=115,y=240,height=50,width=120)

button_tem = tk.Button(text='Temperature', compound=tk.TOP, fg='white', bg='pink2', relief='ridge', font=50, command=temperature)
button_tem.place(x=115,y=315,height=50,width=120)

button_force = tk.Button(text='Force', compound=tk.TOP, fg='white', bg='pink2', relief='ridge', font=50, command=force)
button_force.place(x=115,y=390,height=50,width=120)

root.mainloop()