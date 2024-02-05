import requests

def test_products_get():
    response = requests.get('http://localhost:8000/api/products/')

    print(response.json())
    print(response.status_code)


if __name__ == '__main__':
    test_products_get()
