# import packages
import tkinter as tk
import tkinter.filedialog as fd
import tkinter.messagebox as md
from tkinter.ttk import *

parentClass = tk.Tk
state = False # used to determine if ttkthemes is installed if not then use default tkinter theme

# Uncomment To Use ThemedTk Module if it exist in the global env packages
# try:
# 	from ttkthemed import ThemedTk
# 	parentClass = ThemedTk
# 	state = True
# except Exception as ex:
# 	print("No Module Named ttkThemes")


class Window(parentClass): # root class window
	text_content = None
	filename = ""
	textlength = 1

	def __init__(self, theme="arc"):
		if state:
			parentClass.__init__(self, theme=theme)
		else:
			parentClass.__init__(self)

		# window property
		self.title("Simple Text Editor")
		self.columnconfigure(0, weight=1)
		self.rowconfigure(0, weight=1)
		self.geometry('1200x500')

		# intialize root widget
		self.root = tk.Frame(self)
		self.root.pack(fill=tk.BOTH)

		self.text_content = tk.StringVar()

		# Set Menu and UI
		self.application_menu()
		self.init()
		self.protocol('WM_DELETE_WINDOW', self.close_app) # onDestory Event on UI

	def init(self):
		# creating the textarea
		self.textarea = tk.Text(self.root, height=100, relief="flat", padx=3, pady=3, fg="#0F0F0F", font=('Segoe UI', 13, 'normal'), spacing1=0, wrap=tk.WORD, undo=True)

		# add scrollbar options
		scrollbarY = Scrollbar(self.root, orient="vertical") # scrollbar used for
		scrollbarY.pack(side=tk.RIGHT, fill=tk.Y)
		scrollbarX = Scrollbar(self.root, orient="horizontal")
		scrollbarX.pack(side=tk.BOTTOM, fill=tk.X)
		self.textarea.pack(fill=tk.BOTH, expand=True)

		# bind scroll to textarea
		scrollbarY.config(command=self.textarea.yview)
		scrollbarX.config(command=self.textarea.xview)
		self.textarea.config(yscrollcommand=scrollbarY.set, xscrollcommand=scrollbarX.set)
		self.textarea.columnconfigure(0, weight=1)
		self.textarea.rowconfigure(0, weight=1)

		# bind keyboard shortcuts
		self.textarea.bind('<Control-a>', self.select_all)
		self.bind("<Control-o>", self.open_file)
		self.bind("<Control-n>", self.new_file)
		self.bind("<Control-s>", self.save_file_option)
		self.bind("<Control-q>", self.close_app)


	def application_menu(self):
		# application menu
		app_menu = tk.Menu(self)
		self.config(menu=app_menu)

		# File Menu
		filemenu = tk.Menu(self)
		app_menu.add_cascade(label="File", menu=filemenu)
		filemenu.add_command(label="New", accelerator="Ctlr+N", command=self.new_file)
		filemenu.add_command(label="Open", accelerator="Ctrl+O", command=self.open_file)
		filemenu.add_command(label="Save", accelerator="Ctrl+S", command=self.save_file_option)
		filemenu.add_command(label="Save As...", command=self.save_as_option)
		filemenu.add_separator()
		filemenu.add_command(label="Minimize", command=self.minimize_window)
		filemenu.add_command(label="Exit", accelerator="Ctrl+Q", command=self.close_app)

		# Edit Menu
		edit = tk.Menu(self)
		app_menu.add_cascade(label="Edit", menu=edit)

		def undo(): # undo method
			self.textarea.edit_undo()
		def redo():	# redo method
			self.textarea.edit_redo()

		# Edit Menu
		edit.add_command(label="Undo", accelerator="Ctrl+Z", command=undo)
		edit.add_command(label="Redo", accelerator="Ctrl+Y", command=redo)
		edit.add_command(label="Clear", command=self.clear)
		edit.add_separator()
		edit.add_command(label="Cut", accelerator="Ctrl+X", command=lambda: self.focus_get().event_generate("<<Cut>>"))
		edit.add_command(label="Copy", accelerator="Ctrl+C", command=lambda: self.focus_get().event_generate("<<Copy>>"))
		edit.add_command(label="Paste", accelerator="Ctrl+V", command=lambda: self.focus_get().event_generate("<<Paste>>"))
		edit.add_separator()
		edit.add_command(label="Select All", accelerator="Ctrl-A",command=self.select_all)
		edit.add_command(label="Data/Time", command=self.add_date_time)

		# Format Menu
		format_ = tk.Menu(self)
		app_menu.add_cascade(label="Format", menu=format_)
		wrap = tk.Menu(format_)
		format_.add_cascade(label="Wrap", menu=wrap)
		wrap.add_radiobutton(label="None", command=self.wrap_none)
		wrap.add_radiobutton(label="Character", command=self.wrap_char)
		wrap.add_radiobutton(label="Word", command=self.wrap_word)

		# Info Menu
		help_ = tk.Menu(self)
		app_menu.add_cascade(label="?", menu=help_)
		help_.add_command(label="About", command=self.open_info_button)

	# selection all option
	def select_all(self, event=None):
		self.textarea.tag_add('sel', '1.0', 'end')

	# Add Date Time option
	def add_date_time(self):
		import datetime; self.textarea.insert(tk.INSERT, datetime.datetime.today())
		# Adds a timestamp to the text

	# Wrap Options
	def wrap_none(self): # wrap to none
		self.textarea.config(wrap=tk.NONE)
	def wrap_char(self): # wrap by character
		self.textarea.config(wrap=tk.CHAR)
	def wrap_word(self): # wrap by word
		self.textarea.config(wrap=tk.WORD)

	# Open File Dialog
	def open_file(self, event=None):
		self.filename = fd.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
		with open(self.filename, 'r') as file:
			try:
				self.textarea.delete('1.0', tk.END)
				self.text_content = file.read()
				self.textlength = len(self.text_content) # used for closing the app
				self.textarea.insert(tk.INSERT, self.text_content)
				self.title(self.filename)
			except Exception as e:
				md.showerror("File Parsing", "File Type Unsupported")

	# Create New File
	def new_file(self, event=None):
		self.textarea.delete(0.0, tk.END)
		self.filename = ""
		self.text_content = ""
		self.title("Untitled")

	# Save As option
	def save_as_option(self):
		self.text_content = self.textarea.get(0.0, tk.END)
		savefilename = fd.asksaveasfilename(defaultextension="txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
		self.filename = savefilename

		if len(self.text_content) < 2:
			return
		else:
			with open(self.filename, 'w') as file:
				try:
					self.textlength = len(self.text_content) # for closing the app
					file.write(self.text_content)
					self.title(self.filename)
				except Exception as ex:
					md.showerror("Error Save File", "File Save Error")

	# Save Only file option
	def save_file_option(self, event=None):
		if self.filename ==  "":
			self.save_as_option() # redirect to save dialog
		else:
			self.text_content = self.textarea.get(0.0, tk.END)
			with open(self.filename, 'w') as file:
				try:
					self.textlength = len(self.text_content) # for closing the app
					file.write(self.text_content)
					self.title(self.filename)
				except Exception as ex:
					md.showerror("Error", "Save File Error")

	# Minimize Window
	def minimize_window(self):
		self.wm_state('iconic')
		# Minimize Window

	# Clear textarea
	def clear(self):
		ask = md.askyesno("Clear", "Do You Want To Clear All?")
		if ask:
			self.textarea.delete(0.0, tk.END)
			self.text_content = ""
		else:
			return

	# Exit Application
	def close_app(self, event=None):
		currentTextLength = len(self.textarea.get(0.0, tk.END))

		if currentTextLength != self.textlength:
			result = md.askyesnocancel("Exit App", "Do You Want To Save The File")	# ask user for confirmation exit if file is modified
			if result == None:
				return
			elif result == True:
				self.save_file_option()
			else:
				self.destroy()
		else:
			self.destroy()

	# Close App
	def destroy(self):
		super().destroy()

	# Info Menu Popup (About)
	def open_info_button(self):
		newwindow = tk.Toplevel(self)
		newwindow.title("About")
		newwindow.wm_resizable(False, False)
		newwindow.geometry('215x150')
		root = tk.Frame(newwindow)
		root.columnconfigure(0, weight=1)
		root.rowconfigure(0, weight=1)
		root.pack()
		Label(root, text="About Editor", font=('Helvetica', 16, 'normal')).pack(pady=5, padx=5)
		tk.Message(root, fg="dimgray", text="This is only a dummy Text Editor I made to pass my time and stuff, Its not an full fledge app so it may have a lot of bugs.\n\n#neonzone").pack(pady=5, padx=5)


	# Start Application
	def start(self):
		self.mainloop()


# main
if __name__ == '__main__':
	win = Window(theme='arc') # set theme for ttkthemes if it exist
	win.start()
