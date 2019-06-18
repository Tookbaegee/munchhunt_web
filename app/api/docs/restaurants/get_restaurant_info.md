<p style="padding: 5px; border-radius: 5px; background-color: #FF5555; color: white;"><b>ATTENTION:</b> This method requires Bearer Token Authentication. Read below for details.</p>

`GET /api/restaurants/get/restaurant_info/<string:alias>`  
Returns minimal information about a single restaurant. Useful for getting minimal restaurant information on a map.
## Query Parameters

There are no query parameters. All parameters are included in the URL.

## URL Parameters

'alias' is the alias of a restaurant that is stored in the database. Example:

`/api/restaurants/get/restaurant_info/TB`

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
}
```