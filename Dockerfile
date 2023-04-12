# Base image: ubuntu:22.04
FROM ubuntu:22.04

# ARGs
# https://docs.docker.com/engine/reference/builder/#understand-how-arg-and-from-interact
ARG TARGETPLATFORM=linux/amd64,linux/arm64
ARG DEBIAN_FRONTEND=noninteractive

# neo4j 5.5.0 installation and some cleanup
RUN apt-get update && \
    apt-get install -y wget gnupg software-properties-common && \
    wget -O - https://debian.neo4j.com/neotechnology.gpg.key | apt-key add - && \
    echo 'deb https://debian.neo4j.com stable latest' > /etc/apt/sources.list.d/neo4j.list && \
    add-apt-repository universe && \
    apt-get update && \
    apt-get install -y nano unzip neo4j=1:5.5.0 python3-pip && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Set /cse511 as the working directory
WORKDIR /cse511

# Fetch the dataset and the data loader script
RUN apt-get update && apt-get install -y curl && \
    curl -o yellow_tripdata_2022-03.parquet https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-03.parquet && \
    curl -H "Authorization: token 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" -H "Accept: application/vnd.github.v3.raw" -H "Cache-Control: no-cache" -o data_loader.py -L https://api.github.com/repos/CSE511-SPRING-2023/vconjeev-project-2/contents/data_loader.py

# Install pip and the other required libraries
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install neo4j pandas pyarrow

# Set the Password and the other Neo4j configurations
RUN sed -i 's/#dbms.security.auth_enabled=false/dbms.security.auth_enabled=true/g' /etc/neo4j/neo4j.conf && \
    sed -i 's/#server.default_listen_address=0.0.0.0/server.default_listen_address=0.0.0.0/g' /etc/neo4j/neo4j.conf && \
    neo4j-admin dbms set-initial-password project2phase1

# Install the GDS plugin for Neo4j and configure the settings
RUN curl -L -O https://github.com/neo4j/graph-data-science/releases/download/2.3.1/neo4j-graph-data-science-2.3.1.jar && \
    mv neo4j-graph-data-science-2.3.1.jar /var/lib/neo4j/plugins && \
    chown neo4j:neo4j /var/lib/neo4j/plugins/neo4j-graph-data-science-2.3.1.jar && \
    echo "dbms.security.procedures.unrestricted=gds.*" >> /etc/neo4j/neo4j.conf

# Run the data loader script
RUN chmod +x /cse511/data_loader.py && \
    neo4j start && \
    python3 data_loader.py && \
    neo4j stop

# Expose neo4j ports
EXPOSE 7474 7687

# Start neo4j service and show the logs on container run
CMD ["/bin/bash", "-c", "neo4j start && tail -f /dev/null"]