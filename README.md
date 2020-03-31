# groceri.es

This repository contains all source code for hosting your own groceri.es app.
groceri.es is a webapplication to manage your own recipes, planning your meals
for the week and it automatically creates a groceries list for you to do
shopping.

groceri.es is built by [Jurian Sluiman](https://jurian.slui.mn) and its design 
of groceri.es is opinionated how I perform my meal planning and grocery shopping
in the last years.

## Functional design
The basic idea is you do you groceries weekly and plan the meals ahead for that
week. You can skip days if you plan to eat outdoors, this is your planning for
meals you cook yourself. 

You can quick search a known recipe for a certain day. Otherwise, you can browse
the recipes for a certain day and filter on a variety of options. These recipes
can be planned on a certain day.

Recipes are entered beforehand manually and contains ingredient listings. If you
plan a recipe on a certain day, ingredients are automatically added to your
grocery shopping list.

When you haven't a recipe entered but know what meal you want to schedule at a 
certain day, you can enter it as free text yourself at that day. You can also
provide short notes which can act as guidelines for the meal prep itself. Please
be aware when you schedule meals manually this way, no ingredients are mapped so
you have to add those to the groceries yourself.

The process above is set out in a functional flow diagram below:

![Flow chart of groceri.es functional design]()

### Pantry
Some ingredients are part of you pantry and you buy them in bulk. groceri.es will
automatically map those for you. When you plan a recipe, the pantry items are
assumed to be available and not added to your groceries list. As part of above
flow chart, mind you have to check your pantry and make sure all pantry items as
ingredient are present. If you haven't enough stock, just select the pantry item
to add those to your groceries. 

### Servings
A recipe has a default servings. You are able to change the servings when you
plan your meals. groceri.es will automatically adjust the amount to your needs.

To be more precise, a recipe ingredients listing contains a scale factor. By
default the scale factor is 1, which means that the ingredients are scaled linear
by the servings you need. 

However, some ingredients (like, salt) don't need to double when you double the
servings. You can adjust the scaling factor by the scale parameter. When the
scale for salt, for example, is 0.5, this means doubling the servings means the 
amount of salt will be 1.5 of the original recipe.

Please note you can also scale down servings. Most recipes will serve 4 people,
if your household is only 2, groceri.es will recalculate the ingredients for 2
people. The default servings of a recipe to be calculated, can be set in the 
settings menu.

## Technical design
![UML of the data models]()

Basically the application is a simple CRUD system around recipes and meals. In
the domain model, a **recipe** is a set of instructions for preparing a
particular dish, including the the list of ingredients required. A **meal** is a
dish planned at a specified date.

### Recipe organisation
To help categorize the recipes, a `Category` is offered. A category has a
one-to-many relationship with a recipe, to mark a recipe as starter, main or
desert. This helps greatly in filtering recipes. You can also state which
categories must be shown at default in a recipe listing. If you mainly use
groceri.es for dinner meals, you can filter out drinks, breakfast or lunch.

Another way or organisation is the `Tag`. A tag has a many-to-many relationship
with recipes and adds reusable labels to the recipe. Think for example about the
cuisine (Italian, Indian, French etc) or mark recipes as vegetarian, gluten-free
or whatever organisation you can think of.

### Meal planning
A meal is a planned dish at a certain day. If a recipe is required for
the meal, the meal scheduler will provide the recipe for you. If you don't have
a recipe but you know what to eat, you can simply enter a title of the meal. For
later reference, you can add a note which help you memorize what to prepare.

Note that groceri.es is not opinionated on the time the meal is planned or the
amount of meals you plan at a certain day. This enables users to plan breakfast,
lunch and/or dinner. Or, you can schedule a starter, main course, side
dish and desert at the same day for a large menu. 

### Grocery list and pantry items
When you use the meal scheduler, several recipes will be planned at some days in
your week planning. The ingredients for the recipes will be added to your
grocery list. The quantity of several ingredients is not only based on the
recipe, but also based on your default settings of servings and your (optionally
entered) servings in the meal scheduler.

When using a manually planned dish in the scheduler, you can add grocery items
yourself. Please be aware these manual items aren't linked to a meal. This means
when you remove a meal from the schedule, these ingredients won't disappear from
the grocery list.

Another set of items are the products from your pantry. You can enter pantry
items yourself, but they can be linked from recipes. When you schedule a recipe,
the pantry items won't be added to your groceries automatically, since it is
assumed you have plenty in stock. 

## Source code and software dependencies
The source code is a Flask application with the help of the uwsgi-nginx-flask
docker image. It uses 

## Run groceri.es
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