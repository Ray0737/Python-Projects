import tkinter as tk
root = tk.Tk()

root.title('HOMEWORK-GUI')
root.geometry('600x400+100+100')
root.configure(bg='gray79')

nammelable = tk.Label(text='NAME : ',fg='black',font=100,bg='#EFC445')
nammelable.pack(expand=False,fill='both')
nammelable.place(height=50,width=600)
 
majorlable = tk.Label(text='MAJOR : ',fg='black',font=100,bg='#93D768')
majorlable.pack(expand=False,fill='both')
majorlable.place(x=0,y=55,height=50,width=600)

box1 = tk.Label(text=' ',bg='#D95384')
box1.place(x=0,y=110,height=140,width=140)

box2 = tk.Label(text=' ',bg='#D8525D')
box2.place(x=155,y=110,height=140,width=140)

box3 = tk.Label(text=' ',bg='#CF7195')
box3.place(x=310,y=110,height=140,width=140)

box4 = tk.Label(text=' ',bg='#AA3C2F')
box4.place(x=460,y=110,height=140,width=140)

spsm = tk.Label(text='SPSM ',fg='black',font=100,bg='white')
spsm.pack(expand=False,fill='both')
spsm.place(x=0,y=270,height=50,width=600)

ok = tk.Label(text='OK ',fg='white',font=100,bg='black')
ok.place(x=200,y=330,height=50,width=200)
 
root.mainloop()