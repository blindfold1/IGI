from data_manager import DataManager

class Person:
    def __init__(self, surname, initials, birth_year, birth_date, birth_month):
        self.surname = surname
        self.initials = initials
        self.birth_year = birth_year
        self.birth_date = birth_date
        self.birth_month = birth_month

    def __str__(self):
        return f"{self.surname} {self.initials}, {self.birth_year}-{self.birth_month}-{self.birth_date}"

class Task1(DataManager):
    def __init__(self, data):
        super().__init__(data, csv_file="task1.csv", pickle_file="task1.pkl")
        self.headers = ["surname", "initials", "birth_year", "birth_date", "birth_month"]
        self.sort_keys = ["surname", "initials", "birth_year", "birth_month", "birth_date"]

    def run(self):
        print("Task 1 - Сохранение и загрузка через CSV:")
        self.save_to_csv(self.headers)
        self.load_from_csv(self.headers, Person)
        self.sort_data(self.sort_keys)
        self.display()

        print("\nTask 1 - Сохранение и загрузка через Pickle:")
        self.save_to_pickle()
        self.load_from_pickle()
        self.sort_data(self.sort_keys)
        self.display()

        print("\nTask 1 - Поиск (фамилия 'Иванов'):")
        results = self.search(surname="Иванов")
        for item in results:
            print(item)