# groceri.es

This repository contains all source code for hosting your own groceri.es app.
groceri.es is a webapplication to manage your own recipes, planning your meals
for the week and it automatically creates a groceries list for you to do
shopping.

groceri.es is built by Jurian Sluiman and its design of groceri.es is
opinionated how I perform my meal planning and grocery shopping in the last
years.


## The code

The source code is a Flask application with the help of the uwsgi-nginx-flask
docker image.

## The build

The docker image is meant to be ephemeral, which means the container can be
stopped and thrown away without losing data. The user generated content is
stored in a database, which can be a SQLite database in a docker volume, or a 
(SQL based) database in a linked docker container seperate from this application.

Furthermore it is advised to create a volume container for your image uploads, so
these images are kept seperately from the application container as well.

### Build the image from source code

The image will be available on Docker Hub later, but you can already create the
image yourself with the source code.

Clone the repository first to your local machine

    git clone https://github.com/juriansluiman/groceri.es

Create the docker image from source

    docker build -t groceri.es .

### Run the container

To run an image which you just created, it simply is `docker run`:

    docker run -d --name groceri.es -p 80:80 groceri.es

This will spin up nginx inside the container and will serve the site at port 80
on your host machine. If you want to use a different port, for example 1234, 
change the port argument to `-p 1234:80`.

If you need to run Flask in development setup, you can use the below command to 
run it with the built in webserver. Mind this is not meant to scale for
production!

    docker run -d --rm --name groceri.es -p 1234:80 -v $(pwd)/app:/app \
     -e FLASK_APP=app.py -e FLASK_DEBUG=1 groceri.es \
     flask run --host=0.0.0.0 --port=80