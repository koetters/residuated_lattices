import tkinter as tk
from tkinter import ttk
import platform
import math
from prog import DataStore

class VerticalListWidget(tk.Frame):
  def __init__(self,parent,items):
    super().__init__(parent)
    for i in range(len(items)):
      tk.Label(self,text=items[i],fg='black',bg='white',borderwidth=1,relief='raised').grid(row=i,column=0,sticky="news")

class HorizontalListWidget(tk.Frame):
  def __init__(self,parent,levels,handler):
    super().__init__(parent)
    for i,lvl in enumerate(levels):
      label = tk.Label(self,text=str(lvl),fg='black',bg='white',width=2,borderwidth=1,relief='raised',cursor='hand2')
      label.grid(row=0,column=i,sticky="news")
      label.bind('<Button-1>',lambda event,n=lvl: handler(n))

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
    self.distributions_frame = tk.Frame(self.right_frame,width=math.trunc(0.25*w),height=math.trunc(0.5*h),bg="SlateBlue2")
    self.distributions_frame.grid_propagate(False)
    self.distributions_frame.grid(row=0,column=0,padx=10,pady=5)
    self.distributions_frame.columnconfigure(0,weight=1)
    self.distributions_frame.rowconfigure(0,weight=1)
    self.info_frame = tk.Frame(self.right_frame,width=math.trunc(0.25*w),height=math.trunc(0.5*h),bg="SlateBlue1")
    self.info_frame.grid_propagate(False)
    self.info_frame.grid(row=1,column=0,padx=10,pady=5)
    self.info_frame.columnconfigure(0,weight=1)
#    self.info_frame.rowconfigure(1,weight=1)

    self.ds = DataStore()
    context_list = self.ds.list_context_families()
    self.contexts = None

    self.listbox = tk.Listbox(self.distributions_frame,selectmode=tk.SINGLE)
    self.listbox.config(width=0,height=0)
    for i,contextname in enumerate(context_list):
      self.listbox.insert(i,contextname)
    self.listbox.grid(row=0,column=0)
    self.listbox.bind('<<ListboxSelect>>',self.selection_callback)

    self.root.mainloop()

  def selection_callback(self,event):
    w = event.widget
    index = w.curselection()[0]
    name = w.get(index)
    self.contexts = self.ds.context_family(name)
    self.display_info()

  def display_info(self):
    for widget in self.left_frame.winfo_children():
      widget.destroy()
    for widget in self.info_frame.winfo_children():
      widget.destroy()
    propnames = []
    for level,context in self.contexts.items():
      propnames = context.attributes
      break
    for level,context in self.contexts.items():
      assert len(propnames) == len(context.attributes)
      for i in range(len(propnames)):
        assert propnames[i] == context.attributes[i]
    levels = sorted(self.contexts.keys(),key=int)
    HorizontalListWidget(self.info_frame,levels,self.display_context).grid(row=0,column=0)
    tk.Button(self.info_frame,text="Aggregate",command=self.aggregate).grid(row=1,column=0,sticky="ew")
    tk.Button(self.info_frame,text="Sum",command=self.sum).grid(row=2,column=0,sticky="ew")
    VerticalListWidget(self.info_frame,propnames).grid(row=3,column=0)

  def display_context(self,n):
    context = self.contexts[n]
    propnames = context.attributes
    header = ("n=%s" % n,) + tuple(propnames)
    rows = []
    for profile,number in context.distribution.items():
      if all(isinstance(value,bool) for value in profile):
        rows.append((number,) + tuple(map(lambda v:"x" if v==True else " ",profile)))
      else:
        rows.append((number,) + profile)
    rows = [header] + sorted(rows,reverse=True)

    for widget in self.left_frame.winfo_children():
      widget.destroy()

    self.canvas = tk.Canvas(self.left_frame)
    self.canvas.grid(row=0,column=0)
    self.scrollbar = ttk.Scrollbar(self.left_frame,orient=tk.VERTICAL,command=self.canvas.yview)
    self.scrollbar.grid(row=0,column=1,sticky="ns")
    self.canvas.configure(yscrollcommand=self.scrollbar.set)
    self.table_frame = tk.Frame(self.canvas)
    self.table_frame.grid(row=0,column=0)

    for i in range(len(rows)):
      for j in range(len(rows[0])):
        textcolor = 'black'
        if i==0 or j==0:
          textcolor = 'blue'
        tk.Label(self.table_frame,text=rows[i][j],fg=textcolor,bg='white',borderwidth=1,relief='raised').grid(row=i,column=j,sticky="news")

    self.canvas.create_window((0,0),window=self.table_frame,anchor=tk.NW)
    self.table_frame.update_idletasks()
    bbox = self.canvas.bbox(tk.ALL)
    self.canvas.configure(scrollregion=bbox, width=bbox[2]-bbox[0], height=bbox[3]-bbox[1])

  def aggregate(self):
    levels = sorted(self.contexts.keys(),key=int)
    header = ("",) + tuple(levels)
    attributes = []
    totals = ["all"]
    for n in levels:
      context = self.contexts[n]
      if attributes:
        assert len(attributes) == len(context.attributes)
        for i in range(len(attributes)):
          assert attributes[i] == context.attributes[i]
      else:
        attributes = context.attributes
        assert len(attributes) > 0
      count = 0
      for profile,number in context.distribution.items():
        count += number
      totals.append(count)
    rows = [header,totals]
    for i,m in enumerate(attributes):
      row = [m]
      for n in levels:
        context = self.contexts[n]
        count = 0
        for profile,number in context.distribution.items():
          if profile[i]:
            count += number
        row.append(count)
      rows.append(tuple(row))

    for widget in self.left_frame.winfo_children():
      widget.destroy()

    self.canvas = tk.Canvas(self.left_frame)
    self.canvas.grid(row=0,column=0)
    self.scrollbar = ttk.Scrollbar(self.left_frame,orient=tk.VERTICAL,command=self.canvas.yview)
    self.scrollbar.grid(row=0,column=1,sticky="ns")
    self.canvas.configure(yscrollcommand=self.scrollbar.set)
    self.table_frame = tk.Frame(self.canvas)
    self.table_frame.grid(row=0,column=0)

    for i in range(len(rows)):
      for j in range(len(rows[0])):
        textcolor = 'black'
        if i==0 or j==0:
          textcolor = 'blue'
        tk.Label(self.table_frame,text=rows[i][j],fg=textcolor,bg='white',borderwidth=1,relief='raised').grid(row=i,column=j,sticky="news")

    self.canvas.create_window((0,0),window=self.table_frame,anchor=tk.NW)
    self.table_frame.update_idletasks()
    bbox = self.canvas.bbox(tk.ALL)
    self.canvas.configure(scrollregion=bbox, width=bbox[2]-bbox[0], height=bbox[3]-bbox[1])

  def sum(self):
    levels = sorted(self.contexts.keys(),key=int)
    attributes = []
    for n in levels:
      context = self.contexts[n]
      if attributes:
        assert len(attributes) == len(context.attributes)
        for i in range(len(attributes)):
          assert attributes[i] == context.attributes[i]
      else:
        attributes = context.attributes
        assert len(attributes) > 0
    header = ("",) + tuple(attributes)
    distribution = {}
    for n in levels:
      context = self.contexts[n]
      for profile,number in context.distribution.items():
        if profile in distribution:
          distribution[profile] += number
        else:
          distribution[profile] = number
    rows = []
    for profile,number in distribution.items():
      assert all(isinstance(value,bool) for value in profile)
      rows.append((number,) + tuple(map(lambda v:"x" if v==True else " ",profile)))
    rows = [header] + sorted(rows,reverse=True)

    for widget in self.left_frame.winfo_children():
      widget.destroy()

    self.canvas = tk.Canvas(self.left_frame)
    self.canvas.grid(row=0,column=0)
    self.scrollbar = ttk.Scrollbar(self.left_frame,orient=tk.VERTICAL,command=self.canvas.yview)
    self.scrollbar.grid(row=0,column=1,sticky="ns")
    self.canvas.configure(yscrollcommand=self.scrollbar.set)
    self.table_frame = tk.Frame(self.canvas)
    self.table_frame.grid(row=0,column=0)

    for i in range(len(rows)):
      for j in range(len(rows[0])):
        textcolor = 'black'
        if i==0 or j==0:
          textcolor = 'blue'
        tk.Label(self.table_frame,text=rows[i][j],fg=textcolor,bg='white',borderwidth=1,relief='raised').grid(row=i,column=j,sticky="news")

    self.canvas.create_window((0,0),window=self.table_frame,anchor=tk.NW)
    self.table_frame.update_idletasks()
    bbox = self.canvas.bbox(tk.ALL)
    self.canvas.configure(scrollregion=bbox, width=bbox[2]-bbox[0], height=bbox[3]-bbox[1])

if __name__ == "__main__":
  Application()

