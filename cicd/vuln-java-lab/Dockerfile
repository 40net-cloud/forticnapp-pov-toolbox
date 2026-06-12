# Replace the full file: cicd/vuln-java-lab/Dockerfile

FROM maven:3.8.6-openjdk-11 AS build

WORKDIR /app
COPY pom.xml .
COPY src ./src
RUN mvn -q clean package -DskipTests

FROM eclipse-temurin:8-jre

RUN apt-get update && \
    apt-get install -y curl openssl bash

WORKDIR /app
COPY --from=build /app/target/*.jar app.jar

ENTRYPOINT ["java", "-jar", "app.jar"]
