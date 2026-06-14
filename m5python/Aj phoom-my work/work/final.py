import tkinter as tk
from tkinter import*
from tkinter import ttk
from scipy import constants

root = Tk()
 
root.title('Final')
root.option_add('*font','PSL-omyim 30')
root.geometry('750x900')

conversion_factors = {
    'Length': {
        'meters': {'kilometers': constants.kilo , 'centimeters': constants.centi, 'inches': constants.inch},
        'kilometers': {'meters': 1/constants.kilo, 'centimeters': constants.kilo/constants.centi, 'inches': constants.kilo/constants.inch},
        'centimeters': {'meters': 1/constants.centi, 'kilometers': constants.centi/constants.kilo, 'inches': constants.centi/constants.inch},
        'inches': {'meters': 1/constants.inch, 'kilometers': constants.inch/constants.kilo, 'centimeters': constants.inch/constants.centi},
    },
    # 'Weight': {
    #     'grams': {'kilograms': 1/kilo, 'pounds': gram/pound, 'ounces': gram/ounce},
    #     'kilograms': {'grams': kilo, 'pounds': kilo*pound/gram, 'ounces': kilo*ounce/gram},
    #     'pounds': {'grams': pound/gram, 'kilograms': gram/(kilo*pound), 'ounces': pound/ounce},
    #     'ounces': {'grams': ounce/gram, 'kilograms': gram/(kilo*ounce), 'pounds': ounce/pound},
    # },
}    

def metric():
    global combo_1,combo_2,label_result,result_label,entry_value
    root.destroy()
    root2 = Tk()
    root2.title('Metric')
    root2.option_add('*font', 'Georgia 26')
    root2.geometry('650x700')
    Label(root2, text='การแปลง Metric(SI) Prefixes', fg='purple', width=34).grid(row=0,column=0)
    Label(root2, text='from :').grid(sticky=W)
    entry_value = tk.Entry(root2)
    entry_value.place(x=149,y=50)
    combo_1 = ttk.Combobox(root2, values=["kilometers", "Option 2", "Option 3", "Option 4", "Option 5"])
    combo_1.place(x=149,y=100)
    Label(root2, text='     to :').place(x=0,y=200)
    combo_2 = ttk.Combobox(root2, values=["meters", "Option 2", "Option 3", "Option 4", "Option 5"])
    combo_2.place(x=149,y=200)
    botton_submit =Button(text='SUBMIT',fg='white',bg='pink2')
    botton_submit.place(x=149,y=300)
    Label(root2, text='result :').place(x=0,y=450)
    label_result = tk.Label(root2, text="Result: ")
    label_result.grid(row=3, column=1, padx=10, pady=10)
    result_label = ttk.Label(root2, text=" ", font=('Helvetica', 14))
    result_label.place(x=149,y=400)
    root2.mainloop()
 
def mass():
    root.destroy()
    root3 = Tk()
    root3.title('Mass')
    root3.option_add('*font', 'Georgia 26')
    root3.geometry('550x700')
    Label(root3, text='การแปลง Mass', fg='purple', width=34).pack()
    root3.mainloop()
 
def energy():
    root.destroy()
    root4 = Tk()
    root4.title('Energy')
    root4.option_add('*font', 'Georgia 26')
    root4.geometry('550x700')
    Label(root4, text='การแปลง Energy', fg='purple', width=34).pack()
    root4.mainloop()
 
def tem():
    root.destroy()
    root5 = Tk()
    root5.title('Temperature')
    root5.option_add('*font', 'Georgia 26')
    root5.geometry('550x700')
    Label(root5, text='การแปลง Temperature', fg='purple', width=34).pack()
    root5.mainloop()
 
def force():
    root.destroy()
    root6 = Tk()
    root6.title('Force')
    root6.option_add('*font', 'Georgia 26')
    root6.geometry('550x700')
    Label(root6, text='การแปลง Force', fg='purple', width=34).pack()
    root6.mainloop()
 
topic=Label(root,text='เปลี่ยนหน่วย',bg='pink2')
topic.pack(fill=X)
 
guide=Label(root,text='please select',bg='white')
guide.pack(fill=X)
 
botton_metric= Button(text='SI',compound=TOP,fg='white',bg='pink2',command=metric)
botton_metric.pack()
 
botton_mass= Button(text='Mass',compound=TOP,fg='white',bg='pink2',command=mass)
botton_mass.pack()
 
botton_energy= Button(text='Energy',compound=TOP,fg='white',bg='pink2',command=energy)
botton_energy.pack()
 
botton_tem= Button(text='Temperature',compound=TOP,fg='white',bg='pink2',command=tem)
botton_tem.pack()
 
botton_force =Button(text='Force',compound=TOP,fg='white',bg='pink2',command=force)
botton_force.pack()
 
topic_var = tk.StringVar()


root.mainloop()