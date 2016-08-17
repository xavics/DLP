# DLP (Drone Logistics Platform)

## How to install

### Server

Get the latest git version:

```
git clone https://github.com/xavics/DLP
```

Install dependencies:

```
apt-get install cutycapt
apt-get install nodejs-legacy npm
npm install -g bower

apt-get install python-pip redis-server
pip install -r requirements.txt

```

For install the next dependencies you will need two API keys.
[More info](#environment-variables)

```

export WEATHER_API_KEY=<API_KEY>
export MAPS_API_KEY=<API_KEY>
python manage.py bower install
python manage.py collectstatic
```

### Liquid Galaxy

run script in folder `galaxy_files`

```
cd galaxy_files
bash copy_files.sh <galaxy_ip>
```

## How to run

### Environment variables

Get maps api key from [Google developers](https://developers.google.com/)
Get weather api key from [Openweathermap](http://openweathermap.org/)

```
export MAPS_API_KEY=<API_KEY>
export WEATHER_API_KEY=<API_KEY>
```

### Run server
```
./rundlp <galaxy_ip> <server_ip> 
```
or
```
python manage.py rundlp <galaxy_ip> <server_ip>
```

It will create 5 terminals: Redis Server, Worker1, Worker2, CeleryBeat, Django Server.

### Exit server

`rundlp` will create `exitdlp` in the root of the project.

```
bash exitdlp
```