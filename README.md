# DLP (Drone Logistic Platform)

#How to Install:

Get the last git version of DLP.

pip install requeriments.txt

<!--install geopy-->

python manage.py bower-install

python manage.py collectstatic

done...



#How to run (Under construction.../provisional)

In the root of DLP:

$ bash rundlp 'maps_api_key' 'server_ip' (It will create 4 terminals: Redis Server, Worker1, CeleryBeat, Django Server)
