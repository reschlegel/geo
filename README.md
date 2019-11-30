# Geo location
Create a web service to do basic geolocation. Data engineering exercise.

# Prerequisites
This project makes use of Docker Compose, please ensure that you are running the latest version of Docker and Docker Compose.

  * [Docker/Docker Compose.](https://docs.docker.com/compose/install/)

A REST client such as Postman is also recommended for ease of use in sending GET and POST requests.

  * [Postman](https://www.getpostman.com/downloads/)
  
Follow the installation instructions on the provided links for your OS.

# Setup
1. Clone the github repository.
2. Navigate to the root project folder.
3. Run: ```docker-compose up -d```. If this is the initial run Docker will build the images.

# Usage
Postman is the recommended method for interacting with this app.

The Flask server is running on ```localhost:5000```.

---

Both GET and POST requests are accepted. If accessing through Postman and a POST request, change "Body" to "raw" and select "JSON (application/json)" as the type.

---

The required payload parameters are:
  * key - a Google API access key
  * address - an address

---

### POST Example
![POST example](https://github.com/reschlegel/geo/blob/master/examples/POST%20example.png)

---

### GET Example
![GET example](https://github.com/reschlegel/geo/blob/master/examples/GET%20example.png)
  
Response is a json object the returns the state of the given address.
```
{
  "state": "Georgia"
}
```

# Cleanup
To stop the containers run: ```docker-compose down```

# Common problems
> **I am not receiving a response**

If you submit a request before the PostgreSQL database is ready to accept a connection, you might end up with a hanging request. If this occurs wait 30 seconds and try again.

> **Docker Compose encounters and ERROR with the flask container**

The app should still function, this could depend on your network timeout settings.
