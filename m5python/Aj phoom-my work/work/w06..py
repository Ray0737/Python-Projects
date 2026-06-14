from tkinter import*
root = Tk()
 
root.title('Spin & Play')
root.option_add('*font','Georgia 26')
root.geometry('1275x800')

def exit():
    root.destroy()

def add_record(text):
    global line_count, column_count
    if line_count >= 4:
        column_count += 1
        line_count = 0
    label = Label(root, text=text, font='Georgia 20', anchor='w')
    label.place(x=50 + column_count * 400, y=500 + line_count * 40)
    labels.append(label)
    line_count += 1

def remove_last_record():
    global line_count, column_count, price
    if labels:
        last_label = labels.pop()
        last_label.destroy()
        line_count -= 1
        if line_count < 0:
            column_count -= 1
            line_count = 3
        last_text = last_label.cget("text")
        if last_text in recorded_items:
            recorded_items.remove(last_text)
        if 'Hybs - Making Steak' in last_text:
            price -= 1900
        elif "Prep - 'PREP' LP" in last_text:
            price -= 953
        elif "Numcha - Bloom" in last_text:
            price -=1590
        elif "Anri - Heaven beach" in last_text:
            price -= 1000

        total_price.set(f'Total price : {price}')

def total():
    global price
    if not is_recorded:
        error_message.set("Please record the ordered items first!")
        return

    root2 = Tk()
    root2.title('Total Price')
    root2.option_add('*font', 'Georgia 26')
    Label(root2, text=f'Total price : {price}', fg='purple', width=34).pack()
    root2.mainloop()



def record_order():
    global is_recorded
    if line_count >= 1: 
        is_recorded = True
        error_message.set("") 
        total_button.place(x=450, y=750, height=40, width=350)
    else:
        error_message.set("Please record the ordered items first!")


def hybs_price():
    global price
    price += 1900
    add_record('Hybs - Making Steak     1900-')
    total_price.set(f'Total price : {price}')

def prep_price():
    global price
    price += 953
    add_record("Prep - 'PREP' LP    953-")
    total_price.set(f'Total price : {price}')

def numcha_price():
    global price
    price += 1590
    add_record("Numcha - Bloom      1590-")
    total_price.set(f'Total price : {price}')

def anri_price():
    global price
    price += 1000
    add_record("Anri - Heaven beach     1000-")
    total_price.set(f'Total price : {price}')

 
name=Label(root,text='Serenade Vinyl',bg='LightSkyBlue1',fg='slate blue')
name.grid(row=0,columnspan=5,sticky=NSEW)
 
hybs= PhotoImage(file='Hybs.png')
prep= PhotoImage(file='Prep.png')
numcha= PhotoImage(file='Numcha.png')
anri= PhotoImage(file='Anri.png')
 
hybs_vinyl= Button(text='Hybs - Making Steak',image=hybs,compound=TOP,fg='MediumOrchid1',bg='white',command=hybs_price)
hybs_vinyl.grid(row=2,column=0)
prep_vinyl= Button(text="Prep - 'PREP' LP",image=prep,compound=TOP,fg='dark violet',bg='white',command=prep_price)
prep_vinyl.grid(row=2,column=1)
numcha_vinyl= Button(text='Numcha - Bloom',image=numcha,compound=TOP,fg='PaleVioletRed1',bg='white',command=numcha_price)
numcha_vinyl.grid(row=2,column=2)
anri_vinyl= Button(text='Anri - Heaven beach',image=anri,compound=TOP,fg='DarkGoldenrod1',bg='white',command=anri_price)
anri_vinyl.grid(row=2,column=3)

start=Label(text='Start Recording the Ordered Vinyl Records List',fg='magenta2',bg='floral white',font='Verdana 25')
start.place(x=0,y=320,height=60,width=1275)

list=Label(text='Selected Vinyl Records List',fg='deep pink2',bg='RosyBrown1',font='Verdana 25')
list.place(x=0,y=380,height=50,width=1275)

cancle= Button(text='Cancel the Ordered',fg='navy',bg='white',font='Courier 15',command=remove_last_record)
cancle.place(x=90,y=450,height=40,width=350)

exit_button= Button(text='Exit',fg='DeepSkyBlue2',bg='white',font='Courier 15',command=exit)
exit_button.place(x=490,y=450,height=40,width=300)

record=Button(text='Record the Ordered',fg='blue',bg='white',font='Courier 15',command=record_order)
record.place(x=840,y=450,height=40,width=350)

total_price=StringVar()
total_price.set('Total price : ')
price=0

recorded_items = []
labels = []

line_count = 0
column_count = 0

is_recorded = False

error_message = StringVar()
error_label = Label(root, textvariable=error_message, fg='red', font='Georgia 16')
error_label.place(x=450, y=750, height=40, width=350)

total_button = Button(text='Total the Bill', fg='blue', bg='white', font='Courier 15', command=total)


root.mainloop()
 