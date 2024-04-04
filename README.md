# dora-streamlit
The streamlit app for DoRA

## Running the app
Make sure you have Docker Desktop or an equivalent installed with `docker compose` functionality.
1. clone this project as well as [dora-back](https://github.com/Iodine98/dora-back).
2. build your Docker image of `dora-back` using the tag of `dora-backend` with the appropriate build arguments where you can provide your settings and api keys.
3. build your Docker image of `dora-streamlit` using `docker build -t dora-streamlit`.
4. run `docker compose up` to start all services and access the app using [localhost on port 8501](localhost:8501).

## Modifying the settings
1. run `docker compose down` to stop all services and remove the containers.
2. re-build your docker image of `dora-backend`.
3. run `docker compose up` to start up all services again.
