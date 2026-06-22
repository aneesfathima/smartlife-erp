# Location APIs Documentation

## Overview
These REST API endpoints provide access to countries, states/emirates, and cities data for use in mobile applications and web forms.

---

## 1. Get All Countries

### Endpoint
```
GET /api/v1/countries
```

### Authentication
None required (public endpoint)

### Query Parameters
None

### Request Example
```bash
curl -X GET http://localhost:8091/api/v1/countries
```

### Response Example (200 OK)
```json
{
  "count": 250,
  "countries": [
    {
      "id": 2,
      "name": "United Arab Emirates",
      "code": "AE"
    },
    {
      "id": 3,
      "name": "Afghanistan",
      "code": "AF"
    },
    {
      "id": 233,
      "name": "United States",
      "code": "US"
    }
  ]
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `count` | integer | Total number of countries |
| `countries` | array | Array of country objects |
| `countries[].id` | integer | Unique country ID |
| `countries[].name` | string | Country name |
| `countries[].code` | string | ISO 2-letter country code |

### JavaScript Example
```javascript
const getCountries = async () => {
  try {
    const response = await fetch('http://localhost:8091/api/v1/countries');
    const data = await response.json();

    console.log(`Total countries: ${data.count}`);

    // Find UAE
    const uae = data.countries.find(c => c.code === 'AE');
    console.log('UAE ID:', uae.id); // Output: 2

    return data.countries;
  } catch (error) {
    console.error('Error fetching countries:', error);
  }
};
```

### Python Example
```python
import requests

response = requests.get('http://localhost:8091/api/v1/countries')
data = response.json()

print(f"Total countries: {data['count']}")

# Find UAE
uae = next(c for c in data['countries'] if c['code'] == 'AE')
print(f"UAE ID: {uae['id']}")  # Output: 2
```

---

## 2. Get States/Emirates for a Country

### Endpoint
```
GET /api/v1/states?country_id=<id>
```

### Authentication
None required (public endpoint)

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `country_id` | integer | Yes | ID of the country |

### Request Example
```bash
curl -X GET "http://localhost:8091/api/v1/states?country_id=2"
```

### Response Example (200 OK)
```json
{
  "count": 7,
  "country_id": 2,
  "country_name": "United Arab Emirates",
  "states": [
    {
      "id": 546,
      "name": "Abu Dhabi",
      "code": "AZ"
    },
    {
      "id": 547,
      "name": "Ajman",
      "code": "AJ"
    },
    {
      "id": 548,
      "name": "Dubai",
      "code": "DU"
    },
    {
      "id": 549,
      "name": "Fujairah",
      "code": "FU"
    },
    {
      "id": 550,
      "name": "Ras al-Khaimah",
      "code": "RK"
    },
    {
      "id": 551,
      "name": "Sharjah",
      "code": "SH"
    },
    {
      "id": 552,
      "name": "Umm al-Quwain",
      "code": "UQ"
    }
  ]
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `count` | integer | Total number of states |
| `country_id` | integer | ID of the country |
| `country_name` | string | Name of the country |
| `states` | array | Array of state objects |
| `states[].id` | integer | Unique state ID |
| `states[].name` | string | State/Emirate name |
| `states[].code` | string | State code |

### Error Response (400 Bad Request)
```json
{
  "error": "missing_country_id",
  "error_descrip": "country_id parameter is required"
}
```

### Error Response (404 Not Found)
```json
{
  "error": "country_not_found",
  "error_descrip": "Country with ID 999 not found"
}
```

### JavaScript Example
```javascript
const getStates = async (countryId) => {
  try {
    const response = await fetch(
      `http://localhost:8091/api/v1/states?country_id=${countryId}`
    );
    const data = await response.json();

    console.log(`States in ${data.country_name}:`, data.count);
    return data.states;
  } catch (error) {
    console.error('Error fetching states:', error);
  }
};

// Get UAE emirates
const uaeEmirates = await getStates(2);
```

### Python Example
```python
import requests

response = requests.get(
    'http://localhost:8091/api/v1/states',
    params={'country_id': 2}
)
data = response.json()

print(f"Emirates in {data['country_name']}: {data['count']}")
for state in data['states']:
    print(f"  - {state['name']} (ID: {state['id']})")
```

---

## 3. Get Cities

### Endpoint
```
GET /api/v1/cities?country_id=<id>
GET /api/v1/cities?state_id=<id>
```

### Authentication
None required (public endpoint)

### Query Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `country_id` | integer | Optional* | ID of the country |
| `state_id` | integer | Optional* | ID of the state |

*At least one of `country_id` or `state_id` should be provided. If `state_id` is provided, it takes precedence.

### Request Example - By Country
```bash
curl -X GET "http://localhost:8091/api/v1/cities?country_id=2"
```

### Request Example - By State
```bash
curl -X GET "http://localhost:8091/api/v1/cities?state_id=548"
```

### Response Example (200 OK) - All UAE Cities
```json
{
  "count": 47,
  "cities": [
    {
      "id": 95,
      "name": "Abu Dhabi City",
      "state_id": 546,
      "state_name": "Abu Dhabi",
      "country_id": 2,
      "country_name": "United Arab Emirates"
    },
    {
      "id": 96,
      "name": "Al Ain",
      "state_id": 546,
      "state_name": "Abu Dhabi",
      "country_id": 2,
      "country_name": "United Arab Emirates"
    },
    {
      "id": 112,
      "name": "Dubai Marina",
      "state_id": 548,
      "state_name": "Dubai",
      "country_id": 2,
      "country_name": "United Arab Emirates"
    }
  ]
}
```

### Response Example (200 OK) - Dubai Cities Only
```json
{
  "count": 16,
  "cities": [
    {
      "id": 103,
      "name": "Al Barsha",
      "state_id": 548,
      "state_name": "Dubai",
      "country_id": 2,
      "country_name": "United Arab Emirates"
    },
    {
      "id": 112,
      "name": "Dubai Marina",
      "state_id": 548,
      "state_name": "Dubai",
      "country_id": 2,
      "country_name": "United Arab Emirates"
    },
    {
      "id": 113,
      "name": "Downtown Dubai",
      "state_id": 548,
      "state_name": "Dubai",
      "country_id": 2,
      "country_name": "United Arab Emirates"
    }
  ]
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `count` | integer | Total number of cities |
| `cities` | array | Array of city objects |
| `cities[].id` | integer | Unique city ID |
| `cities[].name` | string | City name |
| `cities[].state_id` | integer/null | State ID (if available) |
| `cities[].state_name` | string/null | State name (if available) |
| `cities[].country_id` | integer/null | Country ID (if available) |
| `cities[].country_name` | string/null | Country name (if available) |

### JavaScript Example
```javascript
// Get all cities in UAE
const getCitiesByCountry = async (countryId) => {
  try {
    const response = await fetch(
      `http://localhost:8091/api/v1/cities?country_id=${countryId}`
    );
    const data = await response.json();
    return data.cities;
  } catch (error) {
    console.error('Error fetching cities:', error);
  }
};

// Get cities in Dubai only
const getCitiesByState = async (stateId) => {
  try {
    const response = await fetch(
      `http://localhost:8091/api/v1/cities?state_id=${stateId}`
    );
    const data = await response.json();
    return data.cities;
  } catch (error) {
    console.error('Error fetching cities:', error);
  }
};

// Usage
const uaeCities = await getCitiesByCountry(2);
const dubaiCities = await getCitiesByState(548);
```

### Python Example
```python
import requests

# Get all cities in UAE
response = requests.get(
    'http://localhost:8091/api/v1/cities',
    params={'country_id': 2}
)
uae_cities = response.json()['cities']
print(f"Total UAE cities: {len(uae_cities)}")

# Get cities in Dubai only
response = requests.get(
    'http://localhost:8091/api/v1/cities',
    params={'state_id': 548}
)
dubai_cities = response.json()['cities']
print(f"Dubai cities: {len(dubai_cities)}")
```

---

## Static UAE Data

For offline use or caching, static UAE data is available in `UAE_STATIC_DATA.json`.

### Usage Example
```javascript
// Import static data (if using module system)
import uaeData from './UAE_STATIC_DATA.json';

// Use static data
console.log('UAE ID:', uaeData.country.id); // 2
console.log('Emirates:', uaeData.states.length); // 7
console.log('Cities:', uaeData.cities.length); // 47

// Find Dubai emirate
const dubai = uaeData.states.find(s => s.name === 'Dubai');
console.log('Dubai ID:', dubai.id); // 548

// Find cities in Dubai
const dubaiCities = uaeData.cities.filter(c => c.state_id === dubai.id);
console.log('Dubai cities:', dubaiCities.length);
```

---

## Complete Integration Example (React Native)

```javascript
import React, { useState, useEffect } from 'react';
import { View, Text, Picker } from 'react-native';

const API_BASE = 'http://localhost:8091';

const LocationSelector = () => {
  const [countries, setCountries] = useState([]);
  const [states, setStates] = useState([]);
  const [cities, setCities] = useState([]);

  const [selectedCountry, setSelectedCountry] = useState(null);
  const [selectedState, setSelectedState] = useState(null);
  const [selectedCity, setSelectedCity] = useState(null);

  // Load countries on mount
  useEffect(() => {
    fetch(`${API_BASE}/api/v1/countries`)
      .then(res => res.json())
      .then(data => setCountries(data.countries))
      .catch(err => console.error('Error loading countries:', err));
  }, []);

  // Load states when country changes
  useEffect(() => {
    if (selectedCountry) {
      fetch(`${API_BASE}/api/v1/states?country_id=${selectedCountry}`)
        .then(res => res.json())
        .then(data => setStates(data.states))
        .catch(err => console.error('Error loading states:', err));
    }
  }, [selectedCountry]);

  // Load cities when state changes
  useEffect(() => {
    if (selectedState) {
      fetch(`${API_BASE}/api/v1/cities?state_id=${selectedState}`)
        .then(res => res.json())
        .then(data => setCities(data.cities))
        .catch(err => console.error('Error loading cities:', err));
    }
  }, [selectedState]);

  return (
    <View>
      <Text>Country</Text>
      <Picker
        selectedValue={selectedCountry}
        onValueChange={(value) => {
          setSelectedCountry(value);
          setSelectedState(null);
          setSelectedCity(null);
        }}
      >
        <Picker.Item label="Select Country" value={null} />
        {countries.map(country => (
          <Picker.Item
            key={country.id}
            label={country.name}
            value={country.id}
          />
        ))}
      </Picker>

      {states.length > 0 && (
        <>
          <Text>State/Emirate</Text>
          <Picker
            selectedValue={selectedState}
            onValueChange={(value) => {
              setSelectedState(value);
              setSelectedCity(null);
            }}
          >
            <Picker.Item label="Select State" value={null} />
            {states.map(state => (
              <Picker.Item
                key={state.id}
                label={state.name}
                value={state.id}
              />
            ))}
          </Picker>
        </>
      )}

      {cities.length > 0 && (
        <>
          <Text>City</Text>
          <Picker
            selectedValue={selectedCity}
            onValueChange={setSelectedCity}
          >
            <Picker.Item label="Select City" value={null} />
            {cities.map(city => (
              <Picker.Item
                key={city.id}
                label={city.name}
                value={city.id}
              />
            ))}
          </Picker>
        </>
      )}
    </View>
  );
};

export default LocationSelector;
```

---

## Error Codes

| Status Code | Error Code | Description |
|-------------|-----------|-------------|
| 400 | `missing_country_id` | country_id parameter is required |
| 400 | `invalid_country_id` | country_id must be a valid integer |
| 400 | `invalid_state_id` | state_id must be a valid integer |
| 404 | `country_not_found` | Country with given ID not found |
| 500 | `server_error` | Internal server error |

---

## Notes

1. **No Authentication Required**: All location endpoints are public and don't require authentication
2. **CORS Enabled**: All endpoints support CORS for cross-origin requests
3. **Caching Recommended**: Location data doesn't change frequently, consider caching on the client side
4. **UAE ID**: United Arab Emirates has ID `2` with code `AE`
5. **Limit**: Cities endpoint returns maximum 1000 records per request

---

## Support

For API issues or questions, please contact the development team or file an issue in the project repository.
