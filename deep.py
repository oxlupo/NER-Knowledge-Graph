from bs4 import BeautifulSoup
import requests
import os
import json
file = open("all_brand", "r", encoding="utf-8")
data = file.read()
data = data.replace("\n", ",")
data = data.split(",")
for i in data:
    i = i.lower()

def get_product(table):
    clean_product = []
    product_list = []
    for td in table:

        a_list = td.find_all("a", href=True)
        for pr in a_list:
            if "product" in str(pr):
                product_list.append(pr.text)
                # print(pr.text)
    for k in product_list:
        d = str(k.replace("\n", ""))

        clean_product.append(d)
    clean_product = clean_product[3:]
    return clean_product


product_dict = {}
list_of_product = list()
for product in data:
    try:
        all_product = []
        if f"{product}.json" in os.listdir('brands'):

            continue
        url = f"https://world.openfoodfacts.org/brand/{product}"
        text = requests.get(url).text
        soup = BeautifulSoup(text, "html.parser")
        page_number = soup.find_all("ul", id="pages")

        for page in page_number:
            num = []
            number = page.find_all("a", href=True)


        if page_number == []:
            with open(f"brands/{product}.json", "w", encoding="utf-8") as f:

                table = soup.find_all("div", id="main_column")
                products = get_product(table)
                all_product.append(products)
                product_dict = {product: all_product}
                json.dump(product_dict, f)
                f.close()
                print(product)
        else:
            for n in number:
                num.append(n.text)
            print("page number:", num)
            num = int(num[-2])
            table = soup.find_all("div", id="main_column")
            products = get_product(table)
            all_product.append(products)


            product_2 = []
            try:
                url = f"https://world.openfoodfacts.org/brand/{product}/{2}"
                text = requests.get(url).text
                soup = BeautifulSoup(text, "html.parser")
                table = soup.find_all("div", id="main_column")
                products = get_product(table)
                product_2.append(products)
                print(2, product, products)

            except Exception:
                continue
            final_list = product_2 + all_product
            with open(f"brands/{product}.json", "w", encoding="utf-8") as f:
                product_dict = {f"{product}": final_list}
                json.dump(product_dict, f)
                f.close()
    except Exception:
        print(Exception)


with open("all_product.json", "w", encoding="utf-8") as f:

    json.dump(product_dict, f)
    f.close()




