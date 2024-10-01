import nltk
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize
from difflib import get_close_matches
import tkinter as tk
from tkinter import messagebox

nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)

# Function to check article usage
def check_articles(tokens):
    errors = []
    vowels = "aeiou"
    for i, word in enumerate(tokens[:-1]):
        if word.lower() == 'a' and tokens[i+1][0].lower() in vowels:
            errors.append(f"Incorrect article: 'a' should be 'an' before '{tokens[i+1]}'.")
        if word.lower() == 'an' and tokens[i+1][0].lower() not in vowels:
            errors.append(f"Incorrect article: 'an' should be 'a' before '{tokens[i+1]}'.")
    return errors

# Function to check comma usage
def check_commas(paragraph):
    errors = []
    # This is a simple approach, looking for specific conjunctions without commas
    conjunctions = ['and', 'but', 'so', 'for', 'yet', 'or', 'nor']
    tokens = paragraph.split()
    
    for i, word in enumerate(tokens[:-1]):
        if word.lower() in conjunctions and (i == 0 or tokens[i-1][-1] != ','):
            errors.append(f"Possible missing comma before '{word}'.")
    return errors

# Function to check the paragraph for grammatical errors
def check_paragraph(paragraph):
    tokens = word_tokenize(paragraph)
    errors = []

    # Define a set of common valid words to skip
    valid_words = set([
        "the", "is", "are", "to", "and", "that", "a", "an",
        "in", "of", "for", "on", "with", "but", "he", "she", 
        "it", "they", "we", "you", "not", "as", "this", "at"
    ])

    for word in tokens:
        if word.lower() in valid_words or not word.isalpha():
            continue
        
        # Check if the word exists in WordNet
        if not wn.synsets(word):
            suggestions = get_close_matches(word, [lemma.name() for syn in wn.all_synsets() for lemma in syn.lemmas()])
            if suggestions:
                errors.append(f"'{word}' is incorrect. Suggestions: {', '.join(suggestions)}")
            else:
                errors.append(f"'{word}' not found in WordNet and no suggestions available.")
    
    # Check for specific grammatical issues
    if "go" in tokens and "yesterday" in tokens:
        errors.append("Incorrect tense: 'go' should be 'went'.")
    if "don't" in tokens:
        errors.append("Incorrect usage: 'don't' should be 'doesn't' for singular subjects.")
    if "was" in tokens and "they" in tokens:
        errors.append("Subject-verb agreement: 'was' should be 'were' with plural 'they'.")
    if "seen" in tokens:
        errors.append("Incorrect form: 'seen' should be 'saw'.")

    # Check article usage
    errors.extend(check_articles(tokens))

    # Check for comma mistakes
    errors.extend(check_commas(paragraph))

    if errors:
        return errors
    else:
        return ["The paragraph is correct."]

# Function to handle the button click event
def check_button_click():
    paragraph = text_input.get("1.0", tk.END).strip()
    if paragraph:
        results = check_paragraph(paragraph)
        messagebox.showinfo("Grammar Checker Results", "\n".join(results))
    else:
        messagebox.showwarning("Input Error", "Please enter a paragraph to check.")

# Set up the GUI
root = tk.Tk()
root.title("Grammar Checker")

# Create a text box for input
text_input = tk.Text(root, height=10, width=50)
text_input.pack(padx=10, pady=10)

# Create a button to check the grammar
check_button = tk.Button(root, text="Check Grammar", command=check_button_click)
check_button.pack(pady=5)

# Start the GUI event loop
root.mainloop()            