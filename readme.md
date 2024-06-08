# Currency Conversion API

This API converts prices to the local currency based on the user's location (150+ countries). It provides exchange rates and currency symbols for easy integration into e-commerce websites.

### Llive url
 https://geo-currency-api.onrender.com

## Endpoints

### 1. Default Currency Conversion

**Endpoint:** `/geo-currency/`

**Method:** `GET`

**Description:** Converts the price from USD to the local currency based on the user's location.

**Response:**
```json
{
    "status": "success",
    "data": {
        "base": "USD",
        "convertedTo": "NGN",
        "rate": 1471.70463884,
        "currency_symbol": "₦"
    },
    "user_location": {
        "country": "Nigeria",
        "countryCode": "NG",
        "city": "Lagos"
    }
}
```

### 2. Specific Currency Conversion
**Endpoint:** `/geo-currency/{currency/}`

**Method:** `GET`

**Description**: Converts the price from the specified currency to the local currency based on the user's location.

**Parameters**:

- **currency**: The currency code to convert from (e.g., EUR, GBP, JPY).
Example: /EUR/

**Response**:
```json
{
    "status": "success",
    "data": {
        "base": "EUR",
        "convertedTo": "NGN",
        "rate": 1631.59510503,
        "currency_symbol": "₦"
    },
    "user_location": {
        "country": "Nigeria",
        "countryCode": "NG",
        "city": "Lagos"
    }
}

```

### Usage
**Default Conversion**: Send a GET request to / to get the conversion rate from USD to the user's local currency.

**Specific Conversion**: Send a GET request to /{currency}/ to get the conversion rate from the specified currency to the user's local currency.

### Installation
To install and run the API, follow these steps:

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/currency-conversion-api.git
    ```
2. Navigate to the project directory:
    ```sh
    cd currency-conversion-api
    ```
3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```
4. Start the API server:
    ```sh
    python manage.py runserver
    ```