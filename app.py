import nltk
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize
from difflib import get_close_matches
import tkinter as tk
from tkinter import messagebox, font

nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)

# Function to check article usage
def check_articles(tokens):
    errors = []
    vowels = "aeiou"
    for i, word in enumerate(tokens[:-1]):
        if word.lower() == 'a' and tokens[i + 1][0].lower() in vowels:
            errors.append((i, f"Incorrect article: 'a' should be 'an' before '{tokens[i + 1]}'."))
        if word.lower() == 'an' and tokens[i + 1][0].lower() not in vowels:
            errors.append((i, f"Incorrect article: 'an' should be 'a' before '{tokens[i + 1]}'."))
    return errors

# Function to check comma usage
def check_commas(paragraph):
    errors = []
    conjunctions = ['and', 'but', 'so', 'for', 'yet', 'or', 'nor']
    tokens = word_tokenize(paragraph)
    
    for i, word in enumerate(tokens[:-1]):
        if word.lower() in conjunctions and (i == 0 or tokens[i - 1][-1] != ','):
            errors.append((i, f"Possible missing comma before '{word}'."))
    return errors

# Function to check the paragraph for grammatical errors
def check_paragraph(paragraph):
    tokens = word_tokenize(paragraph)
    errors = []

    valid_words = set([
        "the", "is", "are", "to", "and", "that", "a", "an",
        "in", "of", "for", "on", "with", "but", "he", "she", 
        "it", "they", "we", "you", "not", "as", "this", "at"
    ])

    for i, word in enumerate(tokens):
        if word.lower() in valid_words or not word.isalpha():
            continue
        
        if not wn.synsets(word):
            suggestions = get_close_matches(word, [lemma.name() for syn in wn.all_synsets() for lemma in syn.lemmas()])
            if suggestions:
                errors.append((i, f"'{word}' is incorrect. Suggestions: {', '.join(suggestions)}"))
            else:
                errors.append((i, f"'{word}' not found in WordNet and no suggestions available."))

    if "go" in tokens and "yesterday" in tokens:
        errors.append((tokens.index("go"), "Incorrect tense: 'go' should be 'went'."))
    if "don't" in tokens:
        errors.append((tokens.index("don't"), "Incorrect usage: 'don't' should be 'doesn't' for singular subjects."))
    if "was" in tokens and "they" in tokens:
        errors.append((tokens.index("was"), "Subject-verb agreement: 'was' should be 'were' with plural 'they'."))
    if "seen" in tokens:
        errors.append((tokens.index("seen"), "Incorrect form: 'seen' should be 'saw'."))

    errors.extend(check_articles(tokens))
    errors.extend(check_commas(paragraph))

    return errors

# Function to highlight errors in the text
def highlight_errors(paragraph, errors):
    text_input.delete("1.0", tk.END)
    text_input.insert(tk.END, paragraph)

    text_input.tag_remove("error", "1.0", tk.END)

    tokens = word_tokenize(paragraph)
    current_pos = 0

    for index, message in errors:
        word = tokens[index]
        start_idx = paragraph.find(word, current_pos)
        end_idx = start_idx + len(word)

        if start_idx != -1:
            text_input.tag_add("error", f"1.0 + {start_idx} chars", f"1.0 + {end_idx} chars")
            current_pos = end_idx

# Function to handle the button click event
def check_button_click():
    paragraph = text_input.get("1.0", tk.END).strip()
    if paragraph:
        errors = check_paragraph(paragraph)
        highlight_errors(paragraph, errors)

        if errors:
            error_messages = "\n".join([msg for _, msg in errors])
            show_message("Grammar Checker Results", error_messages)
        else:
            show_message("Grammar Checker Results", "The paragraph is correct.")
    else:
        show_message("Input Error", "Please enter a paragraph to check.")

# Function to show a message box with a larger size
def show_message(title, message):
    messagebox.showinfo(title, message)

# Set up the GUI with enhanced styling
root = tk.Tk()
root.title("Grammar Checker")
root.geometry("800x600")
root.configure(bg="#e3f2fd")

# Create a custom font for the text input and buttons
text_font = font.Font(family="Arial", size=14)
button_font = font.Font(family="Arial", size=12, weight="bold")
header_font = font.Font(family="Arial", size=24, weight="bold")

# Create a header label
header_label = tk.Label(root, text="Grammar Checker", font=header_font, bg="#1976d2", fg="white", padx=10, pady=10)
header_label.pack(fill=tk.X)

# Create a text box for input with larger dimensions and styled background
text_input = tk.Text(root, height=15, width=90, font=text_font, bg="#ffffff", fg="#000000", padx=10, pady=10, wrap=tk.WORD, bd=2, relief="groove")
text_input.pack(padx=10, pady=20)

# Create a button to check the grammar with some styling
check_button = tk.Button(root, text="Check Grammar", command=check_button_click, font=button_font, bg="#4CAF50", fg="white", padx=20, pady=10, relief="raised", bd=4)
check_button.pack(pady=10)

# Configure tag for highlighting errors (e.g., red color and underlining)
text_input.tag_config("error", foreground="red", underline=True)

# Start the GUI event loop
root.mainloop()
