`GET /api/recommend`  
The recommendation algorithm. Is currently a demo method.
## Query Parameters

Parameter | Description
--------- | ----------
`username` | A username of the user (currently does nothing)
`id` | An id (currently does nothing)

## Example Response

```json
{
    "recommendation": {
        "name": "Taco Bell",
        "alias": "TB",
        "latitude": -100,
        "longitude": 100
    },
    "id": 4
}
```