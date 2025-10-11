FROM gradle:jdk21

WORKDIR /app

COPY settings.gradle.kts gradlew ./
COPY gradle gradle/
COPY app app/

RUN ./gradlew :app:build --no-daemon -x test

FROM openjdk:21-jdk-slim

COPY --from=0 /app/app/build/libs/app-0.1.0.jar /proxy-service.jar

EXPOSE 8000
ENV PORT=8000
ENTRYPOINT ["java", "-jar", "proxy-service.jar"]
