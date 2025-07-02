import os
import json
import re
from symspellpy import SymSpell,Verbosity

def init_symspell():
    sym_spell = SymSpell(max_dictionary_edit_distance=5, prefix_length=7)
    # with open('ML/day_1/ru-100k.txt', 'r', encoding='utf-8') as f:
    with open('/home/hom1e/codes/olproga/ML/input/test/eng.txt', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                word, cnt = line.split()
                cnt = int(cnt)
                sym_spell.create_dictionary_entry(word, cnt)
    return sym_spell

def process_file(input_path, output_path, sym_spell):
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    texts = extract_texts(data)
    corrected_texts = []
    
    for text in texts:
        if text.strip():
            corrected = correct_text(text, sym_spell)
            corrected_texts.append(corrected)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(corrected_texts))

def extract_texts(obj):
    texts = []
    if isinstance(obj, dict):
        if 'text' in obj:
            texts.append(obj['text'])
        for value in obj.values():
            texts.extend(extract_texts(value))
    elif isinstance(obj, list):
        for item in obj:
            texts.extend(extract_texts(item))
    return texts

def correct_text(text, sym_spell):
    tokens = re.findall(r'(\w+|\d+|\W+)', text)
    corrected_tokens = []
    
    for token in tokens:
        if re.match(r'^\w+$', token) and not token.isdigit():
            corrected_tokens.append(correct_word(token, sym_spell))
        else:
            corrected_tokens.append(token)
    
    return ''.join(corrected_tokens)

def correct_word(word, sym_spell):
    if re.search(r'\d', word):
        return word
        
    pref = re.search(r'^[\W_]+', word).group() if re.match(r'^[\W_]+', word) else ''
    suff = re.search(r'[\W_]+$', word).group() if re.search(r'[\W_]+$', word) else ''
    clean_word = word[len(pref):len(word)-len(suff)] if pref or suff else word
    
    was_upper = clean_word.istitle()
    
    suggestions = sym_spell.lookup(clean_word.lower(), Verbosity.CLOSEST, max_edit_distance=4)
    
    if suggestions:
        corrected = suggestions[0].term
        if was_upper:
            corrected = corrected.capitalize()
        return pref + corrected + suff
    return word

def main():
    sym_spell = init_symspell()
    input_dir = 'ML/day_1/input/test'
    # input_dir = 'ML/day_1/input/school'
    output_dir = 'ML/day_1/outputtest'
    # output_dir = 'ML/day_1/output'

    os.makedirs(output_dir, exist_ok=True)
    
    for filename in os.listdir(input_dir):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, f'{os.path.splitext(filename)[0]}_output.txt')
        process_file(input_path, output_path, sym_spell)

if __name__ == '__main__':
    main()
