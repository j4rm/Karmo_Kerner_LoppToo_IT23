import json
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox


class PersonData:
    def __init__(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            self.data = json.load(file)

    def get_total_count(self):
        return len(self.data)

    def get_longest_name(self):
        longest_name = max(self.data, key=lambda x: len(x['nimi'].replace(" ", "")))
        return longest_name['nimi'], len(longest_name['nimi'].replace(" ", ""))

    def get_age(self, birthdate, deathdate=None):
        birth_date = datetime.strptime(birthdate, "%Y-%m-%d")
        if deathdate and deathdate != "0000-00-00":
            death_date = datetime.strptime(deathdate, "%Y-%m-%d")
            return (death_date - birth_date).days // 365
        else:
            today = datetime.today()
            return (today - birth_date).days // 365

    def get_oldest_person(self, alive=True):
        if alive:
            alive_people = [person for person in self.data if person['surnud'] == "0000-00-00"]
            oldest_person = max(alive_people, key=lambda x: self.get_age(x['sundinud']))
        else:
            deceased_people = [person for person in self.data if person['surnud'] != "0000-00-00"]
            oldest_person = max(deceased_people, key=lambda x: self.get_age(x['sundinud'], x['surnud']))
        return oldest_person['nimi'], self.get_age(oldest_person['sundinud'], oldest_person['surnud'])

    def get_count_by_profession(self, profession):
        return len([person for person in self.data if profession.lower() in person['amet'].lower()])

    def get_count_born_in_year(self, year):
        return len([person for person in self.data if person['sundinud'].startswith(str(year))])

    def get_unique_professions_count(self):
        return len(set(person['amet'] for person in self.data))

    def get_name_with_more_than_two_parts(self):
        return len([person for person in self.data if len(person['nimi'].split()) > 2])

    def get_birth_death_same_except_year(self):
        return len([person for person in self.data if person['surnud'] != "0000-00-00" and
                    person['sundinud'][5:] == person['surnud'][5:]])

    def get_alive_and_deceased_count(self):
        alive_count = len([person for person in self.data if person['surnud'] == "0000-00-00"])
        deceased_count = len([person for person in self.data if person['surnud'] != "0000-00-00"])
        return alive_count, deceased_count


def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("JSON failid", "*.json")])
    if not file_path:
        return

    try:
        person_data = PersonData(file_path)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open file: {e}")
        return

    results = {
        "Isikute arv kokku": person_data.get_total_count(),
        "Kõige pikem nimi ja tähemärkide arv": person_data.get_longest_name(),
        "Kõige vanem elav inimene": person_data.get_oldest_person(alive=True),
        "Kõige vanem surnud inimene": person_data.get_oldest_person(alive=False),
        "Näitlejate koguarv": person_data.get_count_by_profession("näitleja"),
        "Sündinud 1997 aastal": person_data.get_count_born_in_year(1997),
        "Erinevate elukutsete arv": person_data.get_unique_professions_count(),
        "Nimi sisaldab rohkem kui kaks nime": person_data.get_name_with_more_than_two_parts(),
        "Sünniaeg ja surmaaega on sama v.a. aasta": person_data.get_birth_death_same_except_year(),
        "Elavaid ja surnud isikud": person_data.get_alive_and_deceased_count(),
    }

    result_text.delete(1.0, tk.END)
    for key, value in results.items():
        if isinstance(value, tuple):
            result_text.insert(tk.END, f"{key}: {value[0]}, {value[1]}\n")
        else:
            result_text.insert(tk.END, f"{key}: {value}\n")


# GUI seadistamine
root = tk.Tk()
root.title("Eesti Isikute andmed")

frame = tk.Frame(root)
frame.pack(pady=10)

open_button = tk.Button(frame, text="Ava JSON fail", command=open_file)
open_button.pack()

result_text = tk.Text(frame, width=100, height=20)
result_text.pack(pady=10)

root.mainloop()
