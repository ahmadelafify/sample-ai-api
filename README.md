## Simple AI API

### Installation
```shell
# Optional: Create virtualenv
pip install -r requirements.txt
cp .env.example .env
# Fill out .env
./scripts/run.sh
```

### How to use API:
```shell
# Using an application like Postman
Setup a request to whichever endpoints: 
  POST to /ask 
  GET to /history
  DELETE to /clear_history 
Add a new Header: "Authorization" with the env.API_KEY
Setup 
```
Ensure Authorization Header
![Headers](https://i.imgur.com/ulbY9Jr.png)

#### Example POST request to /ask
![URL](https://i.imgur.com/oXnddjs.png)
![Body](https://i.imgur.com/byJZtOV.png)
Response
![Response](https://i.imgur.com/sazjJr0.png)

#### Example GET request to /history
![Body](https://i.imgur.com/dueL8Aw.png)
Response
![Response](https://i.imgur.com/Nun9jdz.png)

#### Example DELETE request to /clear_history
![Body](https://i.imgur.com/xzziFSY.png)

#### Screenshots of DB documents:
![Documents](https://i.imgur.com/Tn0ZTJ6.png)

#### Proof of creation time:
![Started](https://i.imgur.com/3jZYYNa.png)
