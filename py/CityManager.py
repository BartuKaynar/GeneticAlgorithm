from City import City


class CityManager:
    def __init__(self):
        self.city_lst = list()

    def add(self, city):
        self.city_lst.append(city)

    def __getitem__(self, index):
        return self.city_lst[index]

    def __len__(self):
        return len(self.city_lst)

    def build_country(self):
        self.add(City(60, 200))
        self.add(City(180, 200))
        self.add(City(80, 180))
        self.add(City(140, 180))
        self.add(City(20, 160))
        self.add(City(100, 160))
        self.add(City(200, 160))
        self.add(City(140, 140))
        self.add(City(40, 120))
        self.add(City(100, 120))
        self.add(City(180, 100))
        self.add(City(60, 80))
        self.add(City(120, 80))
        self.add(City(180, 60))
        self.add(City(20, 40))
        self.add(City(100, 40))
        self.add(City(200, 40))
        self.add(City(20, 20))
        self.add(City(60, 20))
        self.add(City(160, 20))
