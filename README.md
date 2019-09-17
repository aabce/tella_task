# DJANGO/DRF project example
Used technologies 
* REST API
* JWT [ doc ]( https://jpadilla.github.io/django-rest-framework-jwt/ )|[ git ]( https://github.com/jpadilla/django-rest-framework-jwt )
* MongoDB 
    * [djongo](https://github.com/nesdis/djongo)
    * mongoengine
* ElasticSearch
    * [elasticsearch]()
    * [django-elasticsearch-dsl](https://github.com/sabricot/django-elasticsearch-dsl) - Pay attention to Elasticsearch Compatibility section  
* Docker

###Installations and configurations
0. Download Postman to test ([one way](http://ubuntuhandbook.org/index.php/2018/09/install-postman-app-easily-via-snap-in-ubuntu-18-04/))
1. Install docker [ like this ]( https://phoenixnap.com/kb/how-to-install-docker-on-ubuntu-18-04 )
2. Download MongoDB docker image 
    ```
        $ sudo docker pull mongo:latest
    ```
3. Download ElasticSearch docker image 
    ```
        $ sudo docker pull elasticsearch:7.3.2
    ```
4. Create docker network with your_network_name
    ```
        $ sudo docker network create your_network_name
    ```
5. Run elasticsearch image in docker container in new network 
    ```
        $ docker run -d --name elasticsearch --net your_network_name -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" elasticsearch:7.3.2
    ```
6. Run mongo image in docker container in new network 
    ```
        $ docker run -d --name mongo --net your_network_name -p 27017:27017 -p 27018:27018 -p 27019:27019 -e "discovery.type=single-node" mongo:latest
    ```
7. Clone git repository
    ```
        $ git clone https://github.com/aabce/tella_task.git
    ```
8. Create python virtual environment with python3.6> 
9. Activate virtual environment
10. Install/update pip
11. Install dependencies from requirements.txt  
    ```
        $ pip install -r requirements.txt
    ```
12. Createsuperuser 
    ```
        $ python manage.py createsuperuser
    ```
     Enter required user information 
13. Run server with gunicorn
    ```
        $ gunicorn --bind :8000 market.wsgi:application 
    ```

> To index database objects use\
>$ python manage.py search_index --rebuild

###TEST
  - To run unit test
    ```
        $ python manage.py test
    ```    
  - To test API use Postman
    - Get token
    ```
    token url: localhost:8000/api/accounts/login
    returns  : {
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6Im1hcmtldEBnbWFpbC5jb20iLCJleHAiOjE1Njg3MjMxOTQsImVtYWlsIjoibWFya2V0QGdtYWlsLmNvbSJ9.NRcPCRW6w3j5_4FjRYgr7oGZDxoEQwpNwLQWuo268xw"
    }
    ```
    - Post products info
    ```
    url = localhost:8000/api/products/
    Headers: {
        Authorization: JWT token_from_previous_request
    }
    Body-raw-JSON: {
        "title": "Playstation",
        "description": "good tam param pam pam",
        "features": "some interesting features"
    } 
    ```
    - Post products image
    ```
    url = localhost:8000/api/products/
    Headers: {
        Authorization: JWT token_from_previous_request
    }
    form-data: [
        "img": file
    ]
    ```
    - Other urls
    ```
        patch  = localhost:8000/api/products/:id
        delete = localhost:8000/api/products/:id
        get    = localhost:8000/api/products/
        get    = localhost:8000/api/products/?field=value
            field = title or description or features
            value = string
    ```
    
     

    

    

