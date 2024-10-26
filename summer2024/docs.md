# Shore Line East API Documentation

Base URL: `https://api-sle.tren`

## `GET /api/v1/stations/convertIDToStation/<id>`

| Name | Data Type | Example                |
| ---- | --------- | ---------------------- |
| id   | int       | A station number (1-9) |

### Example

```
curl BASE_URL/api/v1/stations/convertIDToStation/9

{
  "success": true,
  "stationName": "New Haven Union Station"
}
```

## `GET /api/{VERSION}/stations/convertStationToID/<name>`

| Name | Data Type | Example                                                                     |
| ---- | --------- | --------------------------------------------------------------------------- |
| name | String    | Full name of a station (ex. `Madison`, `New-Haven-Union-Station`, `Old-Saybrook`) |

### Example

```
curl BASE_URL/api/v1/stations/convertStationToID/New-Haven-State-Street

{
  "success": true,
  "stationID": "2"
}

```

## `POST /api/v1/fares/getRideFare`

| Name       | Data Type | Example                                                                       |
| ---------- | --------- | ----------------------------------------------------------------------------- |
| start      | String    | Any valid station, in English (`New London`, `Old Saybrook`, `Madison`, etc.) |
| end        | String    | Same as above                                                                 |
| isSenior   | boolean   | `true`/`false`, applies the senior citizen discount if `true`                 |
| isOffPeak  | boolean   | `true`/`false`\*                                                              |
| ticketType | String    | `one_way`, `ten_trip`, `monthly`, `monthly_bus`, `school_monthly`             |

### Example

```
curl -X POST BASE_URL/api/v1/fares/getRideFare \
-H "Content-Type: application/x-www-form-urlencoded" \
--data-urlencode "start=New London" \
--data-urlencode "end=Madison" \
--data-urlencode "isSenior=false" \
--data-urlencode "isOffPeak=false" \
--data-urlencode "ticketType=one_way"

{
  "fare": "7.50",
  "comment": null,
  "currency": "USD"
}
```

\* this parameter only applies to trips that involve Metro North, which this API does not support. Setting this value to true or false will not impact the fare cost.


## /api/v1/stations/listAllStations

No parameters. Lists off all stations and their respective IDs.

### Example

```
{
  "New London": "1",
  "Old Saybrook": "2",
  "Westbrook": "3",
  "Clinton": "4",
  "Madison": "5",
  "Guilford": "6",
  "Branford": "7",
  "New Haven State Street": "8",
  "New Haven Union Station": "9"
}
```

## /api/v1/trains/getStationByID/\<id>

| Name | Data Type | Example                                                                     |
| ---- | --------- | --------------------------------------------------------------------------- |
| id | String    | ID of a station, ie. `1`, `4` |

### Example

```
GET /api/v1/trains/getStationByID/5

{
  "generatedAt": 1729910302,
  "showingPastTrains": false,
  "eastbound": {
    "times": [],
    "stops": {
      "currentStation": "Madison",
      "direction": "eastbound",
      "callingAt": [
        "Clinton",
        "Westbrook",
        "Old Saybrook",
        "New London"
      ],
      "terminatesAt": "New London"
    }
  },
  "westbound": {
    "times": [],
    "stops": {
      "currentStation": "Madison",
      "direction": "westbound",
      "callingAt": [
        "Guilford",
        "Branford",
        "New Haven State Street",
        "New Haven Union Station"
      ],
      "terminatesAt": "New Haven Union Station"
    }
  }
}
```