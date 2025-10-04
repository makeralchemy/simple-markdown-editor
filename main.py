import tkinter as tk
from tkinter import PanedWindow, Text, Menu, filedialog, messagebox
from tkinter.font import Font
import re

class MarkdownEditor(tk.Tk):
    def __init__(self):
        super().__init__()

        # --- Constants ---
        self.BG_COLOR = "#2b2b2b"
        self.TEXT_COLOR = "#a9b7c6"
        self.EDITOR_BG = "#3c3f41"
        self.CURSOR_COLOR = "#ffffff"
        self.SASH_COLOR = "#4e5254"
        self.MENU_BG = "#3c3f41"
        self.MENU_FG = "#a9b7c6"
        self.FONT_FAMILY = "Consolas"
        self.FONT_SIZE = 14
        self.H1_COLOR = "#61afef"
        self.CODE_BG = "#45494c"

        # --- Window Setup ---
        self.title("Markdown Editor")
        self.geometry("1200x800")
        self.configure(bg=self.BG_COLOR)

        # --- State Variables ---
        self.current_file = None
        self.is_saved = True

        # --- Initialization ---
        self.create_widgets()
        self.create_menu()
        self.bind_shortcuts()
        self._update_title()
        self.protocol("WM_DELETE_WINDOW", self.quit_app)

        # --- Force window to foreground ---
        self.lift()
        self.attributes('-topmost', True)
        self.after(1000, lambda: self.attributes('-topmost', False))

    def create_widgets(self):
        main_pane = PanedWindow(self, orient=tk.HORIZONTAL, bg=self.BG_COLOR, sashrelief=tk.FLAT, sashwidth=8, bd=0)
        main_pane.pack(fill=tk.BOTH, expand=1, padx=5, pady=5)

        # --- Editor Pane ---
        self.editor = Text(main_pane, wrap='word', undo=True,
                           font=(self.FONT_FAMILY, self.FONT_SIZE),
                           bg=self.EDITOR_BG, fg=self.TEXT_COLOR,
                           insertbackground=self.CURSOR_COLOR,
                           selectbackground="#4a4d50", selectforeground=self.TEXT_COLOR,
                           relief=tk.FLAT, borderwidth=0, padx=10, pady=10)
        main_pane.add(self.editor, stretch="always")

        # --- Preview Pane (as a Text widget) ---
        self.preview = Text(main_pane, wrap='word',
                            font=(self.FONT_FAMILY, self.FONT_SIZE),
                            bg=self.BG_COLOR, fg=self.TEXT_COLOR,
                            relief=tk.FLAT, borderwidth=0, padx=10, pady=10)
        main_pane.add(self.preview, stretch="always")

        # --- Configure Preview Tags ---
        self.preview.tag_configure("h1", font=Font(family=self.FONT_FAMILY, size=int(self.FONT_SIZE * 1.5), weight="bold"), foreground=self.H1_COLOR)
        self.preview.tag_configure("h2", font=Font(family=self.FONT_FAMILY, size=int(self.FONT_SIZE * 1.3), weight="bold"), foreground=self.H1_COLOR)
        self.preview.tag_configure("h3", font=Font(family=self.FONT_FAMILY, size=int(self.FONT_SIZE * 1.1), weight="bold"), foreground=self.H1_COLOR)
        self.preview.tag_configure("bold", font=Font(family=self.FONT_FAMILY, size=self.FONT_SIZE, weight="bold"))
        self.preview.tag_configure("italic", font=Font(family=self.FONT_FAMILY, size=self.FONT_SIZE, slant="italic"))
        self.preview.tag_configure("code", background=self.CODE_BG, font=(self.FONT_FAMILY, self.FONT_SIZE))

        self.preview.config(state=tk.DISABLED)

        self.editor.bind("<<Modified>>", self.on_text_change)
        self.on_text_change() # Initial render

    def on_text_change(self, event=None):
        if self.editor.edit_modified() or event is None:
            if event is not None:
                self.is_saved = False
                self._update_title()

            self.preview.config(state=tk.NORMAL)
            self.preview.delete("1.0", tk.END)

            markdown_text = self.editor.get("1.0", tk.END)
            in_code_block = False

            for line in markdown_text.splitlines():
                if line.strip().startswith("```"):
                    in_code_block = not in_code_block
                    self.preview.insert(tk.END, line + '\n', "code")
                    continue
                
                if in_code_block:
                    self.preview.insert(tk.END, line + '\n', "code")
                    continue

                # Headings
                if line.startswith("# "): self.preview.insert(tk.END, line[2:] + '\n', "h1")
                elif line.startswith("## "): self.preview.insert(tk.END, line[3:] + '\n', "h2")
                elif line.startswith("### "): self.preview.insert(tk.END, line[4:] + '\n', "h3")
                else:
                    # Inline styling
                    self.apply_inline_styles(line + '\n')

            self.preview.config(state=tk.DISABLED)
            if event is not None:
                self.editor.edit_modified(False)

    def apply_inline_styles(self, line):
        # A simple regex-based approach for bold, italic, and inline code
        parts = re.split(r'(\`\`\`.*?\`\`\`|\*\*.*?\*\*|\*.*?\*|\`.*?\`)', line)
        for part in parts:
            if part.startswith('```') and part.endswith('```'): self.preview.insert(tk.END, part[3:-3], "code")
            elif part.startswith('**') and part.endswith('**'): self.preview.insert(tk.END, part[2:-2], "bold")
            elif part.startswith('*') and part.endswith('*'): self.preview.insert(tk.END, part[1:-1], "italic")
            elif part.startswith('`') and part.endswith('`'): self.preview.insert(tk.END, part[1:-1], "code")
            else: self.preview.insert(tk.END, part)

    def create_menu(self):
        menubar = Menu(self, bg=self.MENU_BG, fg=self.MENU_FG, activebackground='#4b4f52', activeforeground=self.MENU_FG, relief=tk.FLAT)
        self.config(menu=menubar)

        file_menu = Menu(menubar, tearoff=0, bg=self.MENU_BG, fg=self.MENU_FG, activebackground='#4b4f52', activeforeground=self.MENU_FG)
        menubar.add_cascade(label="File", menu=file_menu)

        file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Open...", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_separator()
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As...", command=self.save_as_file, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit_app)

    def bind_shortcuts(self):
        self.bind("<Control-n>", self.new_file)
        self.bind("<Control-o>", self.open_file)
        self.bind("<Control-s>", self.save_file)
        self.bind("<Control-S>", self.save_as_file)

    def _update_title(self):
        file_part = self.current_file.split("/")[-1] if self.current_file else "Untitled"
        title = f"{file_part}{' *' if not self.is_saved else ''} - Markdown Editor"
        self.title(title)

    def _check_unsaved(self):
        if not self.is_saved:
            response = messagebox.askyesnocancel("Unsaved Changes", f"Do you want to save changes to {self.current_file or 'Untitled'}?")
            if response is True: return self.save_file()
            elif response is False: return True
            else: return False
        return True

    def new_file(self, event=None):
        if not self._check_unsaved(): return
        self.editor.delete('1.0', tk.END)
        self.current_file = None
        self.is_saved = True
        self._update_title()
        self.on_text_change()

    def open_file(self, event=None):
        if not self._check_unsaved(): return
        filepath = filedialog.askopenfilename(filetypes=[("Markdown Files", "*.md"), ("All Files", "*.*")] )
        if not filepath: return
        try:
            with open(filepath, "r", encoding='utf-8') as f:
                self.editor.delete('1.0', tk.END)
                self.editor.insert('1.0', f.read())
                self.current_file = filepath
                self.is_saved = True
                self._update_title()
                self.on_text_change()
        except Exception as e:
            messagebox.showerror("Error Opening File", str(e))

    def save_file(self, event=None):
        if not self.current_file: return self.save_as_file()
        try:
            with open(self.current_file, "w", encoding='utf-8') as f:
                f.write(self.editor.get("1.0", tk.END))
            self.is_saved = True
            self._update_title()
            return True
        except Exception as e:
            messagebox.showerror("Error Saving File", str(e))
            return False

    def save_as_file(self, event=None):
        filepath = filedialog.asksaveasfilename(defaultextension=".md", filetypes=[("Markdown Files", "*.md"), ("All Files", "*.*")] )
        if not filepath: return False
        self.current_file = filepath
        return self.save_file()

    def quit_app(self, event=None):
        if self._check_unsaved():
            self.destroy()

if __name__ == "__main__":
    app = MarkdownEditor()
    app.mainloop()
