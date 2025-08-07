from csv import DictReader


def get_elements() -> list[dict[str, str]]:
    with open("./src/database/elements.csv") as data:
        dict_reader = DictReader(data)

        list_of_dict = list(dict_reader)

        return list_of_dict


__all__ = ["get_elements"]
