NetConf via REST API

Run Application server in Container

## To Build Docker image

docker build -t netconf .

## To Run 
docker run -it  -p 5000:5000 -v code_path/app/:/app netconf