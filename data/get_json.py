import json
import re

def remove_html_tags(text):
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    return re.sub(clean, ' ', text)

def extract_number(title, keyword):
    """Extract a number from a title string like 'Chapter 1' or 'Book 2'"""
    match = re.search(fr"{keyword} (\d+)", title)
    return match.group(1) if match else ""

def extract_translations_and_titles(input_file_path='al-kafi.json', output_file_path='translations_with_titles.json'):
    with open(input_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    translations_with_titles = []

    def traverse_chapters(chapters, volume_title="", book_number=""):
        for chapter in chapters:
            # Update the volume title and book number if present in the "crumbs"
            if "crumbs" in chapter:
                for crumb in chapter["crumbs"]:
                    if "indexed_titles" in crumb and "en" in crumb["indexed_titles"]:
                        indexed_title = crumb["indexed_titles"]["en"]
                        if indexed_title.startswith("Volume"):
                            volume_title = indexed_title
                        if indexed_title.startswith("Book"):
                            book_number = extract_number(indexed_title, "Book")

            if "chapters" in chapter:
                traverse_chapters(chapter["chapters"], volume_title, book_number)
            else:
                chapter_number = ""
                if "crumbs" in chapter:
                    for crumb in chapter["crumbs"]:
                        if "indexed_titles" in crumb and "en" in crumb["indexed_titles"]:
                            indexed_title = crumb["indexed_titles"]["en"]
                            if indexed_title.startswith("Chapter"):
                                chapter_number = extract_number(indexed_title, "Chapter")

                # Process each verse
                if "verses" in chapter:
                    for verse in chapter["verses"]:
                        translations_list = verse.get("translations", {}).get("en.hubeali", None)
                        hadith_number = verse.get("local_index", "")
                        narrator_chain = verse.get("narrator_chain", {}).get("parts", [])
                        # Extract narrators
                        narrators = [part['text'] for part in narrator_chain if part['kind'] == 'narrator']
                        chain = " -> ".join(narrators)

                        if translations_list and hadith_number:
                            # Join translations list into a single string and remove HTML tags
                            translation_string = "\n".join(translations_list)
                            clean_translation = remove_html_tags(translation_string)
                            clean_title = remove_html_tags(f"{volume_title} - Book {book_number} - Chapter {chapter_number} - Hadith {hadith_number}")
                            entry = {
                                "title": clean_title,
                                "translation": clean_translation,
                                "chain": chain
                            }
                            translations_with_titles.append(entry)

    if "chapters" in data:
        traverse_chapters(data["chapters"])

    with open(output_file_path, 'w', encoding='utf-8') as outfile:
        json.dump(translations_with_titles, outfile, ensure_ascii=False, indent=4)

# Call the function
extract_translations_and_titles()
