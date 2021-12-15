import PPIN as ppin
import Database as PPIdb
import json 



if __name__ == "__main__":

    with open("Datasets/DONTEDIT/ppidb.json", "r") as f:
        data = json.load(f)
    ppidb = PPIdb.Database()
    ppidb.remove_everything()
    count = 0
    for i in data["protiens"]:
        count += 1
        ppidb.insert_protein(data["protiens"][str(i)])
        if count == 500:
            break
    count = 0
    for i in data["interactions"]:
        count += 1
        ppidb.insert_interaction(data["interactions"][str(i)])
        if count == 500:
            break

    ppin = ppin.PPIN(ppidb)