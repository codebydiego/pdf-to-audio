import unittest
from unittest.mock import patch, mock_open, MagicMock
import tkinter as tk
from main import PDFToAudioApp

class TestPDFToAudioApp(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = PDFToAudioApp(self.root)
    
    def tearDown(self):
        self.root.destroy()
    
    @patch('main.filedialog.askopenfilename', return_value='test.pdf')
    @patch('main.PdfReader')
    def test_open_pdf(self, mock_pdf_reader, mock_askopenfilename):
        mock_pdf_reader.return_value.pages = [MagicMock(extract_text=lambda: "Test text")]
        self.app.open_pdf()
        self.assertEqual(self.app.text_widget.get(1.0, tk.END).strip(), "Test text")
    
    @patch('main.filedialog.asksaveasfilename', return_value='test.mp3')
    @patch('main.gTTS')
    def test_convert_to_audio(self, mock_gtts, mock_asksaveasfilename):
        mock_gtts_instance = mock_gtts.return_value
        mock_gtts_instance.save = MagicMock()
        self.app.convert_to_audio("Test text")
        mock_gtts_instance.save.assert_called_with('test.mp3')
    
    @patch('main.messagebox.showerror')
    def test_open_pdf_error(self, mock_showerror):
        with patch('main.filedialog.askopenfilename', return_value=None):
            self.app.open_pdf()
            mock_showerror.assert_not_called()
        
        with patch('main.filedialog.askopenfilename', return_value='test.pdf'):
            with patch('main.PdfReader', side_effect=Exception("Test error")):
                self.app.open_pdf()
                mock_showerror.assert_called_with("Error", "An error occurred: Test error")
    
    @patch('main.messagebox.showerror')
    def test_convert_to_audio_error(self, mock_showerror):
        with patch('main.filedialog.asksaveasfilename', return_value=None):
            self.app.convert_to_audio("Test text")
            mock_showerror.assert_not_called()
        
        with patch('main.filedialog.asksaveasfilename', return_value='test.mp3'):
            with patch('main.gTTS', side_effect=Exception("Test error")):
                self.app.convert_to_audio("Test text")
                mock_showerror.assert_called_with("Error", "An error occurred during audio conversion: Test error")

if __name__ == "__main__":
    unittest.main()
