<p style="padding: 5px; border-radius: 5px; background-color: #FF5555; color: white;"><b>ATTENTION:</b> This method requires Basic Auth Authentication. Read below for details.</p>

`POST /api/tokens`  
Returns a user's token. Valid for one hour upon creation, then a new one will have to be obtained. This should be accounted for in the development of the app.

## Query Parameters

There are no query parameters.

## HTTP Authentication Headers

This method requires the use of HTTP Basic Auth. Basic auth requires a username and password. Depending on the type of app being developed and platform, the HTTP headers will have to be added in different ways. Search up HTTP Basic Auth for Android development if that is what you need, for instance.

## Example Response

The response will be a simple JSON object containing a token:

```json
{
    "token" : "myRandomHexToken"
}
```