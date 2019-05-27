`GET /api/users/<int:id>`  

Gets username of a user with an ID.

## Parameters

`id` is the only parameter, which is the numerical ID of the user.

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