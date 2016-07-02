import re

class WIGFunction:
    def __init__(self, src_lines):
        match = re.match("function ([\w\.\:]+)", src_lines[0])

        self.name = None
        self.subelements = []

        if match:
            self.name = match.group(1)