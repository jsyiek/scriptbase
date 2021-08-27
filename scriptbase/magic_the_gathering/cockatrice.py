import json
import pickle
import xmltodict


class Card:

    def __init__(self, name: str, color: str, manacost: str, cmc: str, Type: str, supertype: list, subtype: list, card_text: str, function: str):
        self.name = name
        self.color = color
        self.manacost = manacost
        self.cmc = int(cmc)
        self.type = Type
        self.supertype = supertype
        self.subtype = subtype
        self.card_text = card_text
        self.function = function

        self.color_id = self.get_color_id()
        self.multicolor_id = list(self.get_multicolor_id())
        self.multicolor_id.sort()
        self.multicolor_id = "".join(self.multicolor_id)

    def get_cmc(self):
        cmc = 0
        for pip in self.manacost:
            if pip.isdigit():
                cmc += int(pip)
            else:
                cmc += 1
        return cmc

    def get_color_id(self):
        unique_pips = ""

        ## Edge cases
        #### Lands
        if self.type == "Land":
            return "C"
        #### Double faced
        if self.manacost is None:
            return "K"
        for pip in self.manacost:
            if pip in "WUBRG" and pip not in unique_pips:
                unique_pips += pip
        if len(unique_pips) > 1:
            return "M"
        elif len(unique_pips) == 0:
            return "C"
        else:
            return unique_pips

    def __repr__(self):
        return f"{self.type} @ {self.manacost} : {self.function}"

    def get_multicolor_id(self):
        if self.color_id != "M":
            return ""
        unique_pips = ""
        for pip in self.manacost:
            if pip in "WUBRG" and pip not in unique_pips:
                unique_pips += pip
        return unique_pips


class CockatriceDatabase:

    path = "dump.dat"

    def __init__(self):
        self.set_data = {
            "W": {},
            "U": {},
            "B": {},
            "R": {},
            "G": {},
            "M": {},
            "C": {},
            "K": {},  # Unknown
        }
        self.set_list = []
        self.card_data = {}

    def add(self, card_obj: Card):
        if card_obj.color_id != "M":
            if card_obj.cmc not in self.set_data[card_obj.color_id]:
                self.set_data[card_obj.color_id][card_obj.cmc] = []

            self.set_data[card_obj.color_id][card_obj.cmc].append(card_obj)
        else:
            if card_obj.multicolor_id not in self.set_data["M"]:
                self.set_data["M"][card_obj.multicolor_id] = {}

            if card_obj.cmc not in self.set_data["M"][card_obj.multicolor_id]:
                self.set_data["M"][card_obj.multicolor_id][card_obj.cmc] = []

            for card_in_data in self.set_data["M"][card_obj.multicolor_id][card_obj.cmc]:
                if card_in_data.name == card_obj.name:
                    return False
            else:
                self.set_data["M"][card_obj.multicolor_id][card_obj.cmc].append(card_obj)
        self.set_list.append(card_obj)
        self.card_data[card_obj.name] = card_obj

    def parse_xml(self, path="DND/DND.xml"):
        with open(path, "r", encoding="utf-8") as F:
            xml_data = F.read().strip()

        parsed = json.loads(json.dumps(xmltodict.parse(xml_data)))['cockatrice_carddatabase']
        # print(parsed)

        for card_dict in parsed["cards"]["card"]:
            supertype_data = card_dict["type"].split(" ")
            supertypes = []
            subtypes = []
            u2014 = False
            for t in supertype_data:
                if t == "\u2014":
                    u2014 = True
                elif u2014:
                    subtypes.append(t)
                else:
                    supertypes.append(t)

            if "token" not in card_dict:
                color = card_dict["color"] if "color" in card_dict else "C"
                non_type_supertypes = supertypes[0:-1] if len(supertypes) > 1 else []
                Type = supertypes[-1]
                card_obj = Card(card_dict["name"], color, card_dict["manacost"], card_dict["cmc"], Type, non_type_supertypes, subtypes, card_dict["text"], "null")
                self.add(card_obj)

    def get_summary_stats(self, data=None):
        if data is None:
            data = self.set_data
        summary_data = {"overall_cmcs": {}, "overall_types":{}, "overall_functions":{}}
        for key in data:
            if key == "M":
                multicolor_info = self.get_summary_stats(data=self.set_data["M"])
                for key, item in multicolor_info.items():
                    ## Treat each color combo as its own color.
                    if "overall" not in key:
                        summary_data[key] = item
                    else:
                        ## To get the summary statistics merged properly, the "overall_type" etc. must be merged
                        ## iteratively.
                        for o_key, o_item in multicolor_info[key].items():
                            if o_key in summary_data[key]:
                                summary_data[key][o_key] += o_item
                            else:
                                summary_data[key][o_key] = o_item
            else:
                summary_data[key] = {"types":{}, "functions":{}, "avg_cmc":0, "num":0, "cmcs":{}}
                for cmc in data[key]:
                    for card_obj in data[key][cmc]:
                        if type(card_obj) == int:
                            breakpoint()
                        if card_obj.type == "Land":
                            continue

                        summary_data[key]["avg_cmc"] += int(cmc)
                        summary_data[key]["num"] += 1

                        ## Local keys
                        if card_obj.function not in summary_data[key]["functions"]:
                            summary_data[key]["functions"][card_obj.function] = 1
                        else:
                            summary_data[key]["functions"][card_obj.function] += 1

                        if card_obj.type not in summary_data[key]["types"]:
                            summary_data[key]["types"][card_obj.type] = 1
                        else:
                            summary_data[key]["types"][card_obj.type] += 1

                        if cmc not in summary_data[key]["cmcs"]:
                            summary_data[key]["cmcs"][cmc] = 1
                        else:
                            summary_data[key]["cmcs"][cmc] += 1


                        ## Global keys
                        if card_obj.function not in summary_data["overall_functions"]:
                            summary_data["overall_functions"][card_obj.function] = 1
                        else:
                            summary_data["overall_functions"][card_obj.function] += 1

                        if card_obj.type not in summary_data["overall_types"]:
                            summary_data["overall_types"][card_obj.type] = 1
                        else:
                            summary_data["overall_types"][card_obj.type] += 1

                        if cmc not in summary_data["overall_cmcs"]:
                            summary_data["overall_cmcs"][cmc] = 1
                        else:
                            summary_data["overall_cmcs"][cmc] += 1
                summary_data[key]["avg_cmc"] = summary_data[key]["avg_cmc"] / summary_data[key]["num"]
        return summary_data

    def load(self):
        with open("OUTPUT/set_data.dat","rb") as F:
            self.set_data = pickle.load(F)

    def define_functions(self, colors=tuple("WUBRGMC"), override_current_func=False, data=None, search=None):
        if data is None:
            data = self.set_data
        for color in colors:
            if color == "M":
                self.define_functions(colors=tuple(self.set_data["M"].keys()), override_current_func=override_current_func, data=self.set_data["M"], search=search)
                continue
            for cmc in data[color]:
                for card_obj in data[color][cmc]:
                    if (card_obj.function != "null" and not override_current_func) and not search:
                        continue
                    if search and card_obj.function != search:
                        continue
                    while True:
                        # print(f"(Card Name): {card_obj.name}")
                        # print(f"(Card Text): {card_obj.card_text}")
                        # print(f"(Current Function): {card_obj.function}")
                        function = input("(Enter Function) >> ")
                        function = function.lower()
                        if function == "n":
                            return
                        elif function == "s":
                            break
                        confirm = input(f"(Please confirm function is: {function} [Y/n]) >> ")
                        if confirm.lower() == "y":
                            card_obj.function = function.lower()
                            break
