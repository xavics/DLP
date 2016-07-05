# DLP (Drone Logistic Platform)

## How to install

Get the latest git version:

```
git clone https://github.com/xavics/DLP
```

Install dependencies:

```
apt-get install nodejs-legacy npm
npm install -g bower

apt-get install python-pip redis-server
pip install -r requeriments.txt

export MAPS_API_KEY=<API_KEY>
python manage.py bower install
python manage.py collectstatic
```

## How to run

### Environment variables

```
export MAPS_API_KEY=<API_KEY>
```

### Run server
```
./rundlp <server_ip> 
```
or
```
python manage.py rundlp <server_ip>
```

It will create 4 terminals: Redis Server, Worker1, CeleryBeat, Django Server.

### Exiting server

Write `y` on the master console.
