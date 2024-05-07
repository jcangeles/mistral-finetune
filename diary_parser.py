from datetime import datetime
from typing import List, Optional
import json
# Converted parser from repo below from C# to Python
# https://github.com/instantiator/anne-frank-diary-parser/tree/main


def fix_spelling(line: str) -> str:
  """Fixes common spelling errors in a diary entry line.

  Args:
      line: A string representing the diary entry line.

  Returns:
      A string with the fixed spelling errors.
  """
  fixes = {
    "2g": "29",
    "APRIF": "APRIL",
  }
  fixed_line = line
  for word in fixes.keys():
    if word.lower() in line.lower():
      fixed_line = fixed_line.replace(word, fixes[word])
  return fixed_line

def split_source(all_lines: List[str]) -> List[dict]:
  """Splits a diary source text into separate diary entries.

  Args:
      all_lines: A list of strings representing all lines in the source text.

  Returns:
      A list of dictionaries representing diary entries, each with "Date" (datetime) and "Lines" (list of strings) keys.
  """
  entries: List[dict] = []
  current_entry: Optional[dict] = None

  for line in map(str.strip, all_lines):
    date = parse_date_line(line)
    if date:
      if current_entry:
        entries.append(current_entry)
      current_entry = {"Date": date}
      current_entry["Lines"] = []
    else:
      if current_entry:
        current_entry["Lines"].append(line)

  if current_entry:
    # Add the last entry
    entries.append(current_entry) 
  return entries

def parse_date_line(line: str) -> Optional[datetime]:
  """Parses a date line from the diary source text.

  Args:
      line: A string representing a potential date line.

  Returns:
      A datetime object if the line is a valid date, otherwise None.
  """
  trimmed = line.strip()
  if trimmed.endswith("1942") or trimmed.endswith("1943") or trimmed.endswith("1944"):
    parts = trimmed.split(",")
    year = int(parts[-1].strip())
    month_day_part = parts[-2].strip()
    month_part, day_part = month_day_part.split(" ", 1)
    month = datetime.strptime(month_part, "%B").month
    day = int(day_part)
    return datetime(year, month, day)
  else:
    return None


def format_paragraphs(entry_lines: list) -> List[str]:
  """Formats paragraphs from a diary entry.

  Args:
      entry: A dictionary representing the diary entry with a "Lines" key containing a list of strings (lines).

  Returns:
      A list of strings representing the formatted paragraphs.
  """
  paragraphs = []
  current_paragraph = ""
  blank_line_counter = 0

  for line in entry_lines:
    # Remove leading and trailing whitespace
    line = line.strip()  
    # Check if line is empty
    if not line:  
      blank_line_counter += 1
    else:
      if blank_line_counter == 0:
        # Not preceded by a blank line, add to current paragraph
        current_paragraph += line if not current_paragraph else f" {line}"
      else:
        # One or more blank lines
        if current_paragraph.endswith(".") or current_paragraph.endswith("?") or current_paragraph.endswith("!") or current_paragraph.endswith("Kitty,"):
          # Start a new paragraph if current one ends with a punctuation (including "Kitty,")
          paragraphs.append(current_paragraph)
          current_paragraph = line
        else:
          # Treat extra blank lines as OCR errors, add line to current paragraph
          current_paragraph += line if not current_paragraph else f" {line}"
      blank_line_counter = 0
  # Add the last paragraph
  paragraphs.append(current_paragraph)  
  return paragraphs


def main():
  file_path = "data/diary.txt"
  lines = open(file_path).read().splitlines()

  # fix spelling errors
  lines = [fix_spelling(line) for line in lines]
  # split source into entries
  entries = split_source(lines)
  # format lines into paragraphs
  reformatted_entries = [
      dict(Date=entry["Date"].strftime("%B %d, %Y"), Lines=format_paragraphs(entry['Lines']))
      for entry in entries
  ]
  # save to json
  with open("data/parsed_diary.json", "w") as fp:
    json.dump(reformatted_entries , fp, indent=4, default=str) 

if __name__ == "__main__":
  main()