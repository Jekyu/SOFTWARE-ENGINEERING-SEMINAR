# ====== STAGE 1: build con Maven ======
FROM maven:3.9-eclipse-temurin-17 AS build

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos solo el pom primero (aprovecha cache de dependencias)
COPY pom.xml .

# Descargamos dependencias (sin compilar aún)
RUN mvn -B dependency:go-offline

# Ahora copiamos el código fuente
COPY src ./src

# Compilamos y empaquetamos la app (saldrá un .jar en target/)
RUN mvn -B clean package -DskipTests

# ====== STAGE 2: runtime (imagen ligera para ejecutar) ======
FROM eclipse-temurin:17-jre-alpine

WORKDIR /app

# Copiamos el jar generado desde la etapa de build
COPY --from=build /app/target/*.jar app.jar

# Puerto por defecto de Spring Boot
EXPOSE 8080

# Comando de arranque
ENTRYPOINT ["java", "-jar", "app.jar"]
