import tkinter as tk
import platform
import math
from prog import ContextSchema
import contexts

class VerticalListWidget(tk.Frame):
  def __init__(self,parent,items):
    super().__init__(parent)
    for i in range(len(items)):
      tk.Label(self,text=items[i],fg='black',bg='white',borderwidth=1,relief='raised').grid(row=i,column=0,sticky="news")

class HorizontalListWidget(tk.Frame):
  def __init__(self,parent,schema,handler):
    super().__init__(parent)
    items = [1,2,3,4,5,6,7,8,9,10,11,12]
    for i in items:
      label = tk.Label(self,text=str(i),fg='black',bg='white',width=2,borderwidth=1,relief='raised',cursor='hand2')
      label.grid(row=0,column=i,sticky="news")
      label.bind('<Button-1>',lambda event,cs=schema,n=i: handler(cs,n))

class TableWidget(tk.Frame):
  def __init__(self,parent,rows):
    super().__init__(parent)
    for i in range(len(rows)):
      for j in range(len(rows[0])):
        textcolor = 'black'
        if i==0 or j==0:
          textcolor = 'blue'
        tk.Label(self,text=rows[i][j],fg=textcolor,bg='white',borderwidth=1,relief='raised').grid(row=i,column=j,sticky="news")

class Application:
  def __init__(self):
    self.root = tk.Tk()
    self.root.title("Residuated Lattices")
    if platform.system() == "Linux":
      self.root.attributes("-zoomed",True)
    else:
      self.root.state("zoomed")
    self.root.update_idletasks()
    w = self.root.winfo_width()
    h = self.root.winfo_height()
    self.left_frame = tk.Frame(self.root,width=math.trunc(0.75*w),height=h,bg="SlateBlue4")
    self.left_frame.grid_propagate(False)
    self.left_frame.grid(row=0,column=0)
    self.left_frame.columnconfigure(0,weight=1)
    self.left_frame.rowconfigure(0,weight=1)
    self.right_frame = tk.Frame(self.root,width=math.trunc(0.25*w),height=h,bg="SlateBlue3")
    self.right_frame.grid_propagate(False)
    self.right_frame.grid(row=0,column=1)
    self.distributions_frame = tk.Frame(self.right_frame,width=math.trunc(0.25*w),height=math.trunc(0.5*h),bg="orange")
    self.distributions_frame.grid_propagate(False)
    self.distributions_frame.grid(row=0,column=0)
    self.distributions_frame.columnconfigure(0,weight=1)
    self.distributions_frame.rowconfigure(0,weight=1)
    self.info_frame = tk.Frame(self.right_frame,width=math.trunc(0.25*w),height=math.trunc(0.5*h),bg="green")
    self.info_frame.grid_propagate(False)
    self.info_frame.grid(row=1,column=0)
    self.info_frame.columnconfigure(0,weight=1)
    self.info_frame.rowconfigure(2,weight=1)

    schemas = contexts.schemas
    self.lookup = {schema.name:schema for schema in schemas}
    assert len(self.lookup) == len(schemas)

    self.listbox = tk.Listbox(self.distributions_frame,selectmode=tk.SINGLE)
    self.listbox.config(width=0,height=0)
    for i,schema in enumerate(schemas):
      self.listbox.insert(i,schema.name)
    self.listbox.grid(row=0,column=0)
    self.listbox.bind('<<ListboxSelect>>',self.selection_callback)

    self.root.mainloop()

  def selection_callback(self,event):
    w = event.widget
    index = w.curselection()[0]
    value = w.get(index)
    schema = self.lookup[value]
#    self.display_context(schema)
    self.display_info(schema)

  def display_info(self,schema):
    propnames = schema.propnames()

    for widget in self.info_frame.winfo_children():
      widget.destroy()
    tk.Label(self.info_frame,text="Hello").grid(row=0,column=0,pady=5)
    HorizontalListWidget(self.info_frame,schema,self.display_context).grid(row=1,column=0)
    VerticalListWidget(self.info_frame,propnames).grid(row=2,column=0)

  def display_context(self,schema,n):
    propnames = schema.propnames()
    ctx = schema.distribution(n)
    header = ("",) + tuple(propnames)
    rows = []
    for profile,number in ctx.items():
      # rows.append((number,) + tuple(map(lambda v:"x" if v==True else " ",profile)))
      rows.append((number,) + profile)
    rows = [header] + sorted(rows,reverse=True)

    for widget in self.left_frame.winfo_children():
      widget.destroy()
    TableWidget(self.left_frame,rows).grid(row=0,column=0)

if __name__ == "__main__":
  Application()

