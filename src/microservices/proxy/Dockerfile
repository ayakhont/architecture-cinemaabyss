FROM openjdk:21-jdk-slim
WORKDIR /app
COPY app/build/libs/app-0.1.0.jar proxy-service.jar
EXPOSE 8000
ENV PORT=8000
ENTRYPOINT ["java", "-jar", "proxy-service.jar"]
