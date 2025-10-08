FROM gradle:jdk21

WORKDIR /app

COPY settings.gradle.kts gradle gradlew app .
RUN ls -la /app
RUN ./gradlew :app:build

COPY app/build/libs/app-0.1.0.jar proxy-service.jar
EXPOSE 8000
ENV PORT=8000
ENTRYPOINT ["java", "-jar", "proxy-service.jar"]
