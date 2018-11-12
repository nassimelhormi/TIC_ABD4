# TIC_ABD4

It's a web architecture for an Escape Game reservation web site.

    1) PHP script that simulates reservations (curl JSON)
    2) Flask API
    3) Reddis Queue to handle database connection
    4) MySQL Replication (Master/Slave)

![Valid XHTML](https://github.com/nassimelhormi/TIC_ABD4/blob/master/schema_archi.png).

![Valid XHTML](https://github.com/nassimelhormi/TIC_ABD4/blob/master/vdm_mcd.png).

## RUN WITH DOCKER-COMPOSE

#### in abd4_api folder

```
$ docker-compose build app
$ docker-compose up
```

#### in generateur IRL Party

```
$ php script.php
```

You can see the that the json are added correctly on the DB Master and on the two Slaves (MySQL replication)
