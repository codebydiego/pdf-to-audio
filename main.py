from gtts import gTTS
import tkinter as tk
from tkinter import filedialog, Text, messagebox
from PyPDF2 import PdfReader

class PDFToAudioApp:
    """
    A class to create a PDF to Audio conversion application using Tkinter.
    """
    def __init__(self, root):
        """
        Initialize the application with the root Tkinter window.
        
        Parameters:
        root (tk.Tk): The root Tkinter window.
        """
        self.root = root
        self.root.title("PDF Reader")
        self.create_widgets()
    
    def create_widgets(self):
        """
        Create and pack the widgets for the application.
        """
        # Button to open PDF file
        self.open_button = tk.Button(self.root, text="Open PDF", command=self.open_pdf)
        self.open_button.pack()
        
        # Text widget to display PDF content
        self.text_widget = Text(self.root, wrap='word')
        self.text_widget.pack(expand=True, fill='both')
        
        # Dropdown menu for language selection
        self.language_var = tk.StringVar(value='en')
        self.language_menu = tk.OptionMenu(self.root, self.language_var, 'en', 'es', 'fr', 'de', 'it')
        self.language_menu.pack()
    
    def open_pdf(self):
        """
        Open a file dialog to select a PDF file, read its content, display the text,
        and convert the text to audio.
        """
        try:
            # Open file dialog to select PDF file
            file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
            if file_path:
                # Read the PDF file
                text = self.read_pdf(file_path)
                # Display the text in the text widget
                self.display_text(text)
                # Convert the text to audio
                self.convert_to_audio(text)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    
    def read_pdf(self, file_path):
        """
        Read the content of a PDF file and extract text from it.
        
        Parameters:
        file_path (str): The path to the PDF file.
        
        Returns:
        str: The extracted text from the PDF file.
        """
        with open(file_path, "rb") as file:
            reader = PdfReader(file)
            # Extract text from each page and concatenate
            text = "".join(page.extract_text() for page in reader.pages)
        return text
    
    def display_text(self, text):
        """
        Display the extracted text in the text widget.
        
        Parameters:
        text (str): The text to display.
        """
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.insert(tk.END, text)
    
    def convert_to_audio(self, text):
        """
        Convert the extracted text to audio and save it as an MP3 file.
        
        Parameters:
        text (str): The text to convert to audio.
        """
        try:
            # Get the selected language
            language = self.language_var.get()
            tts = gTTS(text=text, lang=language)
            
            # Open file dialog to save the audio file
            save_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
            if save_path:
                tts.save(save_path)
                messagebox.showinfo("Success", f"Audio saved successfully at {save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during audio conversion: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFToAudioApp(root)
    root.mainloop()