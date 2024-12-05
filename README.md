# Test project

## How to start

- copy test env

```bash
cp .env.example .env
cp .env.db.example .env.db
```

- Run all services

```bash
docker-compose up -d
```

Now you can open local 

[http://localhost:8000/v1/api/docs](http://localhost:8000/v1/api/docs)

Count insurance

[http://localhost:8000/api/v1/docs#/insurance/calculate_insurance_value_insurance_calculate_get](http://localhost:8000/api/v1/docs#/insurance/calculate_insurance_value_insurance_calculate_get)

## How to work

Update cargo rates by

- JSON
[http://localhost:8000/api/v1/docs#/cargo%20rates/update_cargo_rates_by_json_cargo_rate_update_by_json_post](http://localhost:8000/api/v1/docs#/cargo%20rates/update_cargo_rates_by_json_cargo_rate_update_by_json_post)

- Dict
[http://localhost:8000/api/v1/docs#/cargo%20rates/update_cargo_rates_by_dict_cargo_rate_update_by_dict_post](http://localhost:8000/api/v1/docs#/cargo%20rates/update_cargo_rates_by_dict_cargo_rate_update_by_dict_post)


## How to test
It will be updated later, perhaps :)