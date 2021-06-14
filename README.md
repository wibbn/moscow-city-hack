# Moscow City Hack

## Backend for recomendation service
Recommendation of places for starting a business

## API
### Places

http://84.201.168.52/api/v1/places

*Format:*

+ `type` - business type
+ `address` - the address around which the search will be performed
+ `topk` - number of results

request example
```bash
{
    'type': 'cafe',
    'address': 'Стремянный переулок',
    'topk': 10
}
```

### Heatmap

http://84.201.168.52/api/v1/heatmap

*Format:*
+ `lat` - latitude of the center of the area
+ `lng` - longitude of the center of the area
+ `radius` - radius of the area

request example 
```bash
{
    'lat': 55.731061,
    'lng': 37.579445,
    'radius': 0.005
}
```