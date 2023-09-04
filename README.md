# Surfcast

## **Description**

Surfcast Dashboard is a virtualized application that provides an interface for users to access real-time surfcast powered by [Stormglass API](https://stormglass.io/) at a users chosen coordinate. The project utilizes virtualization with Docker and is structured to run across three separate containers: a frontend, a backend, and a database.

## **Prerequistes**  

This application requires Docker and Docker Compose to run. Ensure both [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/) are installed on your system


## **Installation and Setup**   

To install this application on your system clone the repository using the following command   

```git clone https://github.com/mitzaa/surfcast-dashboard.git```  

Once the repository is cloned navigate to it's directory like so  

```cd surfcast-dashboard```

Once in the correct directory run the following to build the application  

```docker-compose up --build```

Once the build process completes and the services are up, you can access the frontend dashboard at http://localhost:8080 and the backend API at http://localhost:5001


## **Making changes** 

**Frontend:** Navigate to the frontend directory. Introduce changes as needed and rebuild using
```docker-compose build frontend```

**Backend:** Go to the backend directory. Modify Python scripts or routes as required. Ensure any new dependencies are added to requirements.txt. Rebuild using 
```docker-compose build backend``` 

**Database:** Any changes to the database structure or initial data can be made in the db directory.


## **API endpoints**
The stormglass API documentation can be found [here](https://docs.stormglass.io/?_ga=2.257663563.1583304602.1693772014-62783514.1693283963&_gl=1*1iqytci*_gcl_au*MTYzNDI4NDE4MS4xNjkzMjgzOTYz*_ga*NjI3ODM1MTQuMTY5MzI4Mzk2Mw..*_ga_79XDW52F27*MTY5MzgxMTA2My4xMi4wLjE2OTM4MTEwNjMuNjAuMC4w#/)

## **Acknowledgements**

[Nginx](https://www.nginx.com/) serves the frontend  

[Flask](https://flask.palletsprojects.com/en/2.3.x/) for backend development  

[Stormglass API](https://stormglass.io/) for providing the necessary data   


