# aliexpressscraper

Aliexpress product page scraping module. This module does not initiate a selenium web driver instance. It is a group of functions, each function scrapes single data point from the very specific AliExpress product page (e.g. `get_price_variations` gets all product properties combos along with prices and availability for each combo) . However, you have the option to scrape all data points available using `mainScraper` function.

## Usage

To scrape all product page data points use `mainScraper` function example:

```
from aliexpress import mainScraper
myBrowser = webdriver.Firefox()
url = "https://www.aliexpress.com/item/33......"
print(mainScraper(myBrowser, url, logging = True))
```

this prints what mainScraper returns; which is a dictionary including all available data points from the product page structured as per `PRODUCT_DATA` dictionary in the mainScraper definition body: (you can see corresponding function for each data point)

```PRODUCT_DATA = {
    "product_description":get_product_disc(browser, logging),
    "store_name":get_store_name(browser, logging),
    "seller_rating":get_seller_rating(browser, logging),
    "seller_followers":get_seller_followers(browser, logging),
    "product_rating":get_product_rating(browser, logging),
    "number_of_reviews":get_number_reviews(browser, logging),
    "number_of_orders":get_number_orders(browser, logging),
    "shipping_cost":get_shipping_cost(browser, logging),
    "shipping_duration":get_shipping_time(browser, logging),
    "product_specs":get_specs(browser, logging),
    "recommended_urls":get_recomm_urls(browser, logging),
    "product_images":get_all_images(browser, logging),
    "product_variations":get_price_variations(browser,logging)
    }
```
**Note:** `logging` argument is a boolean argument (True/False) which default is True. Use it when verbose is a demand by printing scraping steps and failures (if any), besides logging every step/failure in the file `logging.txt` with date and time.

If you want to scrape a single data point from the product page you need to first get the product page, then use the function for scraping your required data point.

```
from aliexpress import get_product_page, get_seller_followers
myBrowser = webdriver.Firefox()
url = "https://www.aliexpress.com/item/33......"
get_product_page(myBrowser, url, logging)
print(get_seller_followers(seller_followers))
```
which print number of followers for the product seller.
