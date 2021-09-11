from fastapi import FastAPI
#from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.cors import CORSMiddleware
import requests
import random

from urllib.parse import quote

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://foodiefinder.vercel.app/",
    "https://foodiefinder.vercel.app/about"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def get_food(cuisine: str, distance: int, price: str, lat: float, lng: float):

    if distance < 1:
        distance = 1
    elif distance > 20:
        distance = 20
    
    distance = 1609*distance
    
    if price == "2":
        price = "1, 2"
    elif price == "3":
        price = "1, 2, 3"
    elif price == "4":
        price = "1, 2, 3, 4"
    else:
        price = "1"


    API_KEY= "EmNZyvhVKbqUgmrxe_4ifq3lLbTXdIAlel4aYinqHMYP7TXOiu6w2hbfSxghzNgdnZbn0HkyuPgB62KMugT3GK_DghHszLjY_d81yIQgr3FNTRmGceV-nYKcqu0zYXYx"

    API_HOST = 'https://api.yelp.com'
    SEARCH_PATH = '/v3/businesses/search'
    # BUSINESS_PATH = '/v3/businesses/'

    # DEFAULT_TERM = 'dinner'
    # DEFAULT_LOCATION = 'San Francisco, CA'
    SEARCH_LIMIT = 4


    def request(host, path, api_key, url_params=None):
        """Given your API_KEY, send a GET request to the API.
        Args:
            host (str): The domain host of the API.
            path (str): The path of the API after the domain.
            API_KEY (str): Your API Key.
            url_params (dict): An optional set of query parameters in the request.
        Returns:
            dict: The JSON response from the request.
        Raises:
            HTTPError: An error occurs from the HTTP request.
        """
        url_params = url_params or {}
        url = '{0}{1}'.format(host, quote(path.encode('utf8')))
        headers = {
            'Authorization': 'Bearer %s' % api_key,
        }

        print(u'Querying {0} ...'.format(url))

        response = requests.request('GET', url, headers=headers, params=url_params)

        return response.json()





    def search(api_key, term, latitude, longitude, price, radius):
        """Query the Search API by a search term and location.
        Args:
            term (str): The search term passed to the API.
            location (str): The search location passed to the API.
        Returns:
            dict: The JSON response from the request.
        """

        url_params = {
            'categories': term.replace(' ', '+'),
            'latitude': latitude,
            'longitude': longitude,
            'open_now': True,
            'sort_by' : 'rating',
            'price' : price,
            'radius' : radius,
            'limit': SEARCH_LIMIT
        }
        return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)

    x = search(API_KEY, cuisine, lat, lng, price, distance)
    bus = (len(x["businesses"]))
    rand = random.randrange(0,bus)

    return(x["businesses"][rand])