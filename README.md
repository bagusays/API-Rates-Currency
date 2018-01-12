# API-Rates-Currency
API from Webscraping X-Rates. Build with Flask (Python)

### Output
1.  `/` / `/?q=CODE` (default `/` is USD)
```
{
"status": 200,
"updatedTime": "Fri, 12 Jan 2018 16:00:00 GMT",
"result": [
    {
        "Code": "ARS",
        "Name": "Argentine Peso",
        "Price": 0.0014,
        "PriceInverted": 714.08
    },
    {
        "Code": "AUD",
        "Name": "Australian Dollar",
        "Price": 0.000095,
        "PriceInverted": 10518.26
    },
    {
        "Code": "BHD",
        "Name": "Bahraini Dinar",
        "Price": 0.000028,
        "PriceInverted": 35516.77
    },
    {
        "Code": "BWP",
        "Name": "Botswana Pula",
        "Price": 0.000739,
        "PriceInverted": 1353.53
    },
    {
        "Code": "BRL",
        "Name": "Brazilian Real",
        "Price": 0.000241,
        "PriceInverted": 4152.88
    },
    .....
    ....
```

1.  `/specify?from=CODE&to=CODE` (to get code, you can access "/specify")
```
  {
    "result": [
        {
            "Code": "IDR",
            "Name": "Indonesian Rupiah",
            "Price": 0.000075,
            "PriceInverted": 13367.809469,
            "To": "USD"
        }
    ],
    "status": 200,
    "updatedTime": "Fri, 12 Jan 2018 14:49:00 GMT"
  }
