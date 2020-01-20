![codingnomads](https://user-images.githubusercontent.com/15733809/72739771-5b29d480-3b72-11ea-8557-159161501289.png)

# CodingNomads Mentor Portal

A web application for managing student and mentor relationships.  Mentors can see students progress and log one-on-one support.

## Installing / Getting started

Requirements:
```
Docker version 19.03.5
docker-compose version 1.25.0
```



Clone the repository:
```shell
$ git clone git@github.com:rdesmond/codingnomads_mentor_app.git
```

Build docker images for flask app and database:
```shell
$ docker-compose build
```

Run flask server and database in detached mode:
```shell
$ docker-compose up -d
```

Navigate to http://localhost:5001/ping


If the server is live the response in the browser should be:
```
{
  "message": "pong", 
  "status": "success!"
}
```



## Developing

After making changes to the code you may need to rebuild the images:
```shell
docker-compose up -d --build
```

You can also rebuild database from the command line:
```shell
docker-compose exec mentor-portal python main.py recreate_db
```

To seed the database with test users from command line:
```shell
docker-compose exec mentor-portal python main.py seed_db
```

### Testing

To run tests:
```shell
docker-compose exec mentor-portal python -m pytest "application/tests"
```



## Features

* Mentors can log support activity for their students.
* Mentors can view student progress in online corses.


## Configuration



## Contributing




## Licensing

