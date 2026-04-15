FROM maven:3.8.6-openjdk-11 AS build

WORKDIR /app
COPY pom.xml .
COPY src ./src
RUN mvn -q clean package -DskipTests

# 🔥 Use MUCH older base image
FROM ubuntu:16.04

# 🔥 Install older vulnerable packages
RUN apt-get update && \
    apt-get install -y \
    openjdk-8-jre \
    openssl \
    curl \
    bash

WORKDIR /app
COPY --from=build /app/target/*.jar app.jar

ENTRYPOINT ["java", "-jar", "app.jar"]
