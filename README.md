# This Application contains a simple social media api endpoints


## Requirements

To run this application locally, you need to have Docker and Docker Compose installed on your system.

### Installing Docker and Docker Compose

- Docker: Follow the instructions for your operating system on the official Docker website: [Install Docker](https://docs.docker.com/get-docker/)

- Docker Compose: Docker Compose is included with Docker Desktop for Windows and macOS. For Linux systems and older versions of Docker Desktop, you may need to install Docker Compose separately. Follow the instructions here: [Install Docker Compose](https://docs.docker.com/compose/install/)

## Running the Application

Once you have Docker and Docker Compose installed, you can run the application by following these steps:

1. Clone this repository to your local machine.

2. Navigate to the project directory in your terminal.

3. Run the following command to build the Docker containers:

    ```bash
    docker-compose -f local.yml build
    ```

4. After the build process completes, start the Docker containers by running:

    ```bash
    docker-compose -f local.yml up
    ```

5. Once the containers are up and running, you can access the API endpoints using your web browser or a tool like Postman.

## Accessing the API

After the containers are running, you can access the API at the following URL:


## Notes
Make sure their is no port conflicts , web will run on 8000 port and db will bind with 5432
