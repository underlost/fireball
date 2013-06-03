#Fireball

A Pintrest/Pinry clone working on Heroku. I love the open source clone of Pintrest, Pintry. The only issue I have with it, is due to Heroku's platform restrictions, its near impossible to get the application to work on it. Fireball is a proof on concept to demonstrate how its possible to build something similar, using Pillow for thumbnail image creation and Amazon's S3 as storage. 

There are very few examples of Django's new custom [user model](https://docs.djangoproject.com/en/dev/releases/1.5/#configurable-user-model) in the wild, so I also decided to experiment with that by using a custom model (core.Profile) and adding a few extra fields.