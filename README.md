# TensorFlow Model Deployment with Docker and Kubernetes — Showcasing AI/ML application in the microservice architecture
In this project, I will explore the process of building and deploying a deep learning application using Docker and Kubernetes — a powerful, cutting-edge open-source platform that automates the deployment, scaling, and orchestration of containerized applications at scale. More specifically, the project will demonstrate how to deploy an AI/ML model (e.g., a TensorFlow-based MNIST classifier) in the microservice architecture. The project is divided into two parts: In the first part, the official TensorFlow Serving image is used to build and deploy the containerized application. In the second part, the steps for containerizing the application from scratch are outlined.

## Clone the project

    git clone <repository-url>
    cd <repository-folder>
    
## Part 1: Using official TensorFlow Serving image
### Prerequisites
- Docker
- Minikube
- Python 3 (virtual environment)
- Git

### Setup Instructions

1. **Create a virtual environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
2. **Run the classifier code and save the model**

    ```bash
    python3 mnist-classifier.ipynb 
    ```
3. **Deploy the TensorFlow model using Docker**
    ```bash
    cd TF_serving_image_based_service/
    sudo docker run -d --name serving_base -p 8501:8501 \
        -e MODEL_NAME=mymodel \
        -v $(pwd)/mymodel:/models/mymodel \
        tensorflow/serving
    ```
4. **Check the model status**
    ```bash
    curl http://localhost:8501/v1/models/mymodel
    ```
5. **Verify logs**
    ```bash
    sudo docker logs serving_base
    ```
6. **To make prediction request at the serving container**
    ```bash
    cd client_request/
    python3 request.py
    ```
7. **To stop and remove the container** 
    ```bash
    sudo docker stop serving_base  
    sudo docker rm serving_base 
    ```
8. **Deploy the TensorFlow model to Kuburnetes**
    - Start the TensorFlow Serving container: 
        ```bash
        sudo docker run -d --name serving_base tensorflow/serving 
        ```
    - Copy the model to the container: 
        ```bash
        cd TF_serving_image_based_service/
        sudo docker cp ./mymodel serving_base:/models/mymodel 
        ```
    - To log in to Docker Hub: 
        ```bash
        sudo docker login –u <docker_username> 
        ```
    - Committed the container with a new image: 
        ```bash
        sudo docker commit --change "ENV MODEL_NAME mymodel" serving_base <docker_username>/mymodel-serving 
        ```
    - Push the Image to Docker Hub: 
        ```bash
        sudo docker push <docker_username>/mymodel-serving 
        ```
    - To Deploy the Application:
        *Prepare the deployment YAML specification*
        ```bash
        cd TF_serving_image_based_service/
        kubectl apply –f deployment.yml>
        ```
    - To check deployment and service:
        ```bash
        kubectl get pods -A
        kubectl get svc -A
        kubectl get deployment
        ```
    - To Display URL of the Service:  
        ```bash
        minikube ip 
        minikube service <service_name> --url 
        ```
## Part 2: Build and Deploy from the scratch

### Setup Instructions:

1. **Train the model**
    - Train the MNIST classifier model and save it in `.h5` format. 
        ```bash
        python3 mnist-classifier.ipynb
        ```
        Ensure the trained model is saved in the respective path

2. **Prepare project files**
    ```bash
    cd custom_image_based_service/
    ``` 
    Create the following files in the project directory:
    - **`app.py`**: Contains the Flask API or serving script.
    - **`Dockerfile`**: Defines how to build the Docker image.
    - **`requirements.txt`**: Lists the required Python dependencies.
    
4. **Build Docker Image locally**
    ```bash
    docker build -t mnist-classifier-service:v1 
    ```
5. **To tag Docker Image**
    ```bash
    docker tag mnist-classifier-service:v1 <docker_username>/mnist-classifier-service:v1 
    ```
6. **To deploy the container Locally**
    ```bash
    docker run -p 5000:5000 <docker_username>/mnist-classifier-service:v1 
    ```
5. **To push Docker Image to Docker Hub**
    ```bash
    docker login -u <docker_username>
    docker push <docker_username>/mnist-classifier-service:v1
    ```
6. **Deployment of Kubernetes Service**
    ```bash
    cd custom_image_based_service/
    ``` 
    - Prepare the deployment YAML specification
    - Apply the deployment:
        ```bash
        kubectl apply -f deployment.yml
        ```
