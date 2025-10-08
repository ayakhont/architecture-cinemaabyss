FROM openjdk:21-jdk-slim
WORKDIR /app
COPY build/proxy-service.jar proxy-service.jar
EXPOSE 8000
ENV PORT=8000
ENTRYPOINT ["java", "-jar", "proxy-service.jar"]
