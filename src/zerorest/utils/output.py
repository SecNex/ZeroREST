class Output:
    def __init__(self, indent: int = 0):
        self.indent = indent

    def __folder(self, item: dict):
        print(" " * self.indent + " + " + item["name"] + " (" + item["id"] + ") [Folder] (" + str(len(item["children"])) + " children)")
        for child in self.item["children"]:
            Output(child, self.indent + 4)

    def __file(self, item: dict):
        print(" " * self.indent + " - " + item["name"] + " (" + item["id"] + ") [File]")

    def print(self, item: dict):
        if item["type"] == "folder":
            self.__folder(item)
        else:
            self.__file(item)