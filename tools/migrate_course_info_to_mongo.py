import json
import glob
from pymongo import MongoClient

MAJOR_DIR = "/srv/pyflowchart/majors"

def get_json_data(path):
    with open(path, "r") as jsonfile:
        return json.loads(jsonfile.read())

def main():
    client = MongoClient()
    db_name = "cpslo-catalog"
    db = client[db_name]

    json_files = glob.glob(MAJOR_DIR + "/*.json")
    json_data = [get_json_data(path) for path in json_files]
    new_json_data = []

    for catalog in json_data:
        found_catalog = False
        dept = None
        course_data = []

        for k,v in catalog.items():
            if not found_catalog:
                dept = k.split()[0]
                found_catalog = True

            v["course_number"] = int(k[-3:])
            course_data.append(v)

        db[dept].insert_many(course_data)


if __name__ == "__main__":
    main()

