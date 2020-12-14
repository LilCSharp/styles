import requests
import math
import json

# API-endpoint for makeup site
URL = "http://makeup-api.herokuapp.com/api/v1/products.json"

class Product(object):
    def __init__(self, product_json):
        self.name = product_json["Name"]
        self.brand = product_json["Brand"]
        self.price = product_json["Price"]
        self.recipe = product_json["Recipe"]

    def __repr__(self):
        return self.name

class ProductClient(object):
    # Might need to add __init__ later
    def __init__(self):
        f = open("./flask_app/data_files/data.json", "r")
        self.data = json.load(f)
        #self.data = requests.get(url = URL).json()
        self.length = len(self.data)
        self.pages = math.ceil(self.length / 100)

    def get_all(self):
        #self.data = requests.get(url = URL).json()
        f = open("./flask_app/data_files/data.json", "r")
        self.data = json.load(f)
        self.length = len(self.data)
        self.pages = math.ceil(self.length / 100)

    def get_by_id(self, ids):
        results = []

        for i in range(0, len(ids)):
            for j in range(0, self.length):
                if str(self.data[j]['id']) == ids[i]:
                    results.append(self.data[j])
                    break
        
        return results

    def get_best_color(self, color):
        rec_ids = []        

        for i in range(0, self.length):
            for j in range(0, len(self.data[i]['product_colors'])):
                value = 0
                for k in range(1, len(self.data[i]['product_colors'][j]['hex_value']), 2):
                    try:
                        v = int(self.data[i]['product_colors'][j]['hex_value'][k:k+2], 16)
                        value += v**2
                    except Exception:
                        continue
                
                value = math.sqrt(value)

                if abs(color - value) < 25:
                    rec_ids.append(str(self.data[i]['id']))
                    break
        
        return rec_ids

    def get_page(self, page_number):
        """
        Retrieves 100 products from the Makeup API using a supplied url,
        and returns a list of makeup products correspoding to the set 
        of entries in the API with index range [100*page_number - 100,
        100*page_number)
        """
        if (100 * page_number) >= self.length:
            return self.data[(100 * page_number - 100):(self.length)]
        else:
            return self.data[(100 * page_number - 100):(100 * page_number)]

    def search(self, search_string):
        """
        Searches for a product by brand name or by name and returns a
        list of products to which the supplied search_string applies
        """
        self.get_all()
        results = []

        for i in range(0, self.length):
            if self.data[i]['name'].lower().find(search_string) != -1:
                results.append(self.data[i])
        
        self.data = results
        self.length = len(self.data)
        self.pages = math.ceil(self.length / 100)

    # May need function for filtering
    def filter(self, brands, types):
        self.data = []
        
        brand_length = len(brands)
        type_length = len(types)

        if brand_length > 0 and type_length > 0: 
            for i in range(0, brand_length):
                brands[i] = brands[i].replace(" ", "+")

                for j in range(0, type_length):
                    types[j] = types[j].replace(" ", "+")

                    url = URL + "?brand=" + brands[i] + "&product_type=" + types[j]
                    self.data = self.data + requests.get(url = url).json()
        
        elif brand_length > 0:
            for i in range(0, brand_length):
                brands[i].replace(" ", "+")

                url = URL + "?brand=" + brands[i]
                self.data = self.data + requests.get(url = url).json()

        else:
            for i in range(0, type_length):
                types[i].replace(" ", "+")

                url = URL + "?product_type=" + types[i]
                self.data = self.data + requests.get(url = url).json()

        self.length = len(self.data)
        self.pages = math.ceil(self.length / 100)

    # May need function for recommendations later