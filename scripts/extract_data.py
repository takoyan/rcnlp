import pandas as pd

if __name__ == "__main__":
    f = open("../etc/txt/item_list.csv", "r")
    loop = 0
    item_name = []
    caption = []
    for line in f:
        a = line.split(";")
        item_name.append(a[1])
        # caption.append(a[1])
        loop = loop + 1
    df = pd.DataFrame({"item_name": item_name})
    df.to_csv("../etc/txt/item_name_list_.csv", header=False, index=False)
    print("finish")