import requests
#
# # def test_products_get():
# #     response = requests.get('http://localhost:8000/api/products/')
# #
# #     print(response.json())
# #     print(response.status_code)
# #
# #
# # if __name__ == '__main__':
# #     test_products_get()
#
#
# def test_store_get():
#     response = requests.get('http://localhost:8000/api/stores/')
#
#     print(response.json())
#     print(response.status_code)
#
#
# if __name__ == '__main__':
#     test_store_get()


def test_top_selling_products():
    response = requests.get('http://localhost:8000/api/top_selling_products/')

    print(response.json())
    print(response.status_code)

if __name__ == '__main__':
    test_top_selling_products()