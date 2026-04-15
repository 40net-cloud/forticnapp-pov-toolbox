# Stage 1 - Build the Java app
FROM maven:3.8.6-openjdk-11 AS build

WORKDIR /app
COPY pom.xml .
COPY src ./src
RUN mvn -q clean package -DskipTests

# Stage 2 - Runtime image
# Using an existing Java 11 runtime image from Eclipse Temurin
FROM eclipse-temurin:11-jre-focal

WORKDIR /app
COPY --from=build /app/target/*.jar app.jar

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "app.jar"]
