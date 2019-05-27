`POST /api/register`  
Registers a user with Munchhunt. 

## JSON Data

This method requires the sending of JSON data. Here is an example of the data that must be sent:

```json
{
    "username" : "myusername",
    "email" : "myemail@example.com",
    "password" : "myverysecurepassword"
}
```

## Query Parameters

There are no query parameters.

## Example Response

The response will be a simple JSON object containing the information of the user:

```json
{
    "id" : 53,
    "user" : "myusername"
}
```