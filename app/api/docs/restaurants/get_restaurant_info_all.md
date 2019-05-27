<p style="padding: 5px; border-radius: 5px; background-color: #FF5555; color: white;"><b>ATTENTION:</b> This method requires Bearer Token Authentication. Read below for details.</p>

`GET /api/restaurants/get/restaurant_info_all/<string:alias>`  
Returns detailed information about a single restaurant.
## Query Parameters

There are no query parameters. All parameters are included in the URL.

## URL Parameters

'alias' is the alias of a restaurant that is stored in the database. Example:

`/api/restaurants/get/restaurant_info_all/TB`

## HTTP Bearer Token Header

This method requires the use of a bearer token in HTTP headers. This is obtained initially through the [get token API endpoint](/app/api/tokens.html) and expires after one hour.

Depending on the type of app being developed and platform, the HTTP headers will have to be added in different ways. Search up HTTP Basic Auth for Android development if that is what you need, for instance.

## Example Response

The response will be in the following format:

```json
{
    "status":"success",
    "name": "Taco Bell",
    "alias": "TB",
    "latitude": 100,
    "longitude": -50,
    "phone": 666-666-6666,
    "price": "$",
    "direction": "direction",
    "time": "time",
    "hours": {
        "sunday" : "8AM-8PM",
        "monday" : "8AM-8PM",
        "tuesday" : "8AM-8PM",
        "wednesday": "8AM-8PM",
        "thursday": "8AM-8PM",
        "friday": "8AM-8PM",
        "saturday": "8AM-8PM"
    },
    "menu": [
    {
        "name" : "Taco",
        "description" : "It's a taco",
        "itemType" : "Mexican",
        "price" : "$3.99",
    },
    {
        ...
    }
    ] 
}
```

NOTES: 

`"menu"` is an array of menu items.

If there is no `"hour"` or `"menu"` in the database, it will not be included in the JSON result.