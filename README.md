# osp-api

RESTful API for making the OSP database programmatically accessible.

The OSP Explorer uses this project; the frontend communicates with this
backend/REST API.

## Getting started

`pip install -r requirements.txt`

### Docker

Build and run with `sudo docker-compose up --build`, though if you add yourself
to the `docker` group (`sudo usermod -aG docker $(whoami)`) you don't need to
use `sudo`.

I recommend testing with these `httpie` commands (`sudo apt install httpie`) to
see caching in action:

```
http get http://localhost:8000/v1/titles?limit=50&offset=100
http get http://localhost:8000/v1/titles?offset=100&limit=50
```

Notice that the above outputs the same task ID (that's good, the query is being
cached!).
