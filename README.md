# Hyperspace Navigator Droid
Streamlit chat bot for finding shortest hyperspace jump plots in the Star Wars Universe.

[![Intro Video](https://res.cloudinary.com/dqjkf4zsf/image/upload/v1714781412/intro_astro_nav_youtube_thumbnail_ttp0ka.jpg)](https://youtu.be/LStzjNd4Q8A)


## Try it out
Jump to the public [demo](https://astro-droid.streamlit.app)

## Run Locally
- Install [poetry](https://python-poetry.org)
- Create a .env file in the root folder and paste the following (but replace with your own OpenAI key):
```
OPENAI_API_KEY="sk-..."
NEO4J_URI="neo4j+s://8a741169.databases.neo4j.io"
NEO4J_USER="read_only"
NEO4J_PASSWORD="read_only"
NEO4J_DATABASE="neo4j"
```
Neo4j Credentials are read only to a hosted database pre-loaded with unofficial Star Wars Galaxy data from [SWGalaxyMap](http://www.swgalaxymap.com) and [Wookepedia](https://starwars.fandom.com/wiki/Main_Page). 
Alternatively, see the dump/ folder for a database copy you can upload to your own instance. [See official Neo4j docs](https://neo4j.com/docs/aura/auradb/importing/import-database/) for details on how to upload dump files.

- Finally run: 
```
poetry install
poetry run streamlit run hyperspace_navigator_droid/main.py
```

## Suggestions and issues
Open a new [repo issue](https://github.com/jalakoo/hyperspace_navigator_droid/issues)
