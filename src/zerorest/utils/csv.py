import os
import csv

# def create_csv_sites(site):
#     if not os.path.exists("csv"):
#         os.makedirs("csv")
#     if not os.path.exists("csv/sites.csv"):
#         with open("csv/sites.csv", "w", newline="") as csvfile:
#             writer = csv.writer(csvfile, delimiter=";")
#             writer.writerow(["Name", "ID"])
#     with open("csv/sites.csv", "a", newline="") as csvfile:
#         writer = csv.writer(csvfile, delimiter=";")
#         writer.writerow([site["displayName"], site["id"]])

# def create_csv_items(o: dict):
#     for item in o["items"]:
#         create_csv_item(o["site"], o["drive"], item)
#         for child in item["children"]:
#             create_csv_item(o["site"], o["drive"], child)

# def create_csv_item(site: str, drive: str, item: dict):
#     if not os.path.exists("csv"):
#         os.makedirs("csv")
#     if not os.path.exists("csv/items.csv"):
#         with open("csv/items.csv", "w", newline="") as csvfile:
#             writer = csv.writer(csvfile, delimiter=";")
#             writer.writerow(["Site", "Drive", "Name", "ID", "Type", "Path"])
#     with open("csv/items.csv", "a", newline="") as csvfile:
#         writer = csv.writer(csvfile, delimiter=";")
#         writer.writerow([site, drive, item["name"], item["id"], item["type"], item["path"]])

class CSV:
    def __init__(self, path: str, columns: list, overwrite: bool = False):
        self.path = path
        self.columns = columns
        self.overwrite = overwrite
        self.__create()

    def __create(self):
        if not os.path.exists(os.path.dirname(self.path)):
            os.makedirs(os.path.dirname(self.path))
        if not os.path.exists(self.path) or self.overwrite:
            with open(self.path, "w", newline="") as csvfile:
                writer = csv.writer(csvfile, delimiter=";")
                writer.writerow(self.columns)

    def append(self, row: list):
        with open(self.path, "a", newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=";")
            writer.writerow(row)