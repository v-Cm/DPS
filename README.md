# vconjeev-project-2

This README contains the steps and commands used to set up a Kubernetes cluster using Minikube, deploy a ZooKeeper service, and a Kafka deployment on the cluster. It also includes the steps for verifying the communication between Kafka and ZooKeeper.

## Prerequisites
Before starting, ensure that the following are installed on your system (The commands below were ran on an Ubuntu 22.10 system):

* ### Docker (installed the [latest version](https://docs.docker.com/engine/install/ubuntu/))
* ### Minikube
    > To install the latest minikube stable release on x86-64 Linux using binary download:
    ```
    $ curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
    $ sudo install minikube-linux-amd64 /usr/local/bin/minikube
    ```
* ### kubectl
    > Minikube can download the appropriate version of kubectl and you should be able to use it like this:
    ```
    $ minikube kubectl -- get po -A
    $ alias kubectl="minikube kubectl --"
    ```

## Steps
* Add the user to the 'docker' group (ignore if already present)
    ```
    $ sudo usermod -aG docker $USER && newgrp docker
    ```
* Start Minikube using the command:
    ```
    $ minikube start
    ```
* Verify that Minikube is running correctly using the command:
    ```
    $ minikube status
    ```
* Create two yaml files named `zookeper-setup.yaml` and `kafka-setup.yaml`, and create services and deployments in both of them.
* Deploy the ZooKeeper service using the command:
    ```
    $ kubectl apply -f zookeeper.yaml
    ```
* Deploy the Kafka deployment and service using the command:
    ```
    $ kubectl apply -f kafka.yaml
    ```
* Verify that the Kafka deployment and service have been deployed correctly using the commands:
    ```
    $ kubectl get deployments
    $ kubectl get services
    ```
* To verify that Kafka can communicate with ZooKeeper, create a Kafka topic using the command:
    ```
    $ kubectl exec -it kafka-deployment-<pod-id> -- kafka-topics --create --zookeeper zookeeper-service:2181 --replication-factor 1 --partitions 1 --<topic-name>
    ```
  Replace <pod-id> with the ID of the Kafka pod and <topic-name> with a topic name of your choice.
* Verify that the Kafka topic has been created correctly using the command:
    ```
    $ kubectl exec -it kafka-deployment-<pod-id> -- kafka-topics --list --zookeeper zookeeper-service:2181
    ```
  Replace <pod-id> with the ID of the Kafka pod.
* Now to produce and consume messages, run the following command to start a Kafka console producer:
    ```
    $ kubectl exec -it kafka-deployment-<pod-id> -- kafka-console-producer --broker-list localhost:9092 --topic <topic-name>
    ```
  This will open up a console where you can type in messages to send to the <topic-name> topic. Type a message and hit enter.
* In another terminal window, run the following command to start a Kafka console consumer:
    ```
    $ kubectl exec -it kafka-deployment-<pod-id> -- kafka-console-consumer --bootstrap-server localhost:9092 --topic <topic-name> --from-beginning
    ```
  This will start a Kafka console consumer that will read messages from the <topic-name> topic. You should now be able to read the message from the producer.
* To test Zookeeeper's communication with Kafka, enter the Zookeeper pod's shell:
    ```
    $ kubectl exec -it zookeeper-0 -- /bin/bash
    ```
    Inside the Zookeeper's CLI run the command:
    ```
    $ zookeeper-shell localhost:2181
    ls /brokers/topics
    ```
  This should list the <topic-name> which you created a few steps ago which indicates both Kafka and Zookeeper could communicate well.
  
## Conclusion
Up until this point of the project, we have successfully set up a Kubernetes cluster using Minikube, deployed a ZooKeeper service, and a Kafka deployment on the cluster. We have also verified that Kafka can communicate with ZooKeeper by creating a Kafka topic and verifying its existence.
