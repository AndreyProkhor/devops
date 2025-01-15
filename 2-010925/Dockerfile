# # FROM jelastic/maven:3.9.5-openjdk-21 as firststage

# # LABEL try_number="1-st try"

# # MAINTAINER "ANDREW"

# # WORKDIR /app

# # COPY pom.xml .
# # COPY src ./src

# # RUN mvn package


# # FROM openjdk:25-slim-bookworm 

# # WORKDIR /app

# # COPY --from=firststage /app/target/hello-world-0.0.1-SNAPSHOT.jar .

# FROM maven:3-eclipse-temurin-21 as build

# RUN mkdir /app

# COPY . /app

# WORKDIR /app

# RUN mvn package -DskipTests

# RUN jar xf target/hello-world-0.0.1-SNAPSHOT.jar

# RUN jdeps --ignore-missing-deps -q \
#     --recursive \
#     --multi-release 21 \
#     --print-module-deps \
#     --class-path 'BOOT-INF/lib/*' \
#     target/hello-world-0.0.1-SNAPSHOT.jar > deps.info

# RUN jlink \
#     --add-modules $(cat deps.info) \
#     --strip-debug \
#     --compress 2 \
#     --no-header-files \
#     --no-man-pages \
#     --output /myjre

# RUN ls -l /myjre/bin


# FROM alpine:latest

# ENV JAVA_HOME=/myjre
# ENV PATH=$JAVA_HOME/bin:$PATH

# COPY --from=build /myjre $JAVA_HOME

# WORKDIR /app

# COPY --from=build /app/target/hello-world-0.0.1-SNAPSHOT.jar /app/

FROM maven:3-eclipse-temurin-21 as build

RUN mkdir /app

COPY . /app

WORKDIR /app

RUN mvn package -DskipTests

RUN jar xf target/hello-world-0.0.1-SNAPSHOT.jar

RUN jdeps --ignore-missing-deps -q \
    --recursive \
    --multi-release 21 \
    --print-module-deps \
    --class-path 'BOOT-INF/lib/*' \
    target/hello-world-0.0.1-SNAPSHOT.jar > deps.info

RUN jlink \
    --add-modules $(cat deps.info) \
    --strip-debug \
    --compress 2 \
    --no-header-files \
    --no-man-pages \
    --output /myjre

RUN ls -l /myjre/bin


FROM debian:bookworm-slim

ENV JAVA_HOME=/myjre
ENV PATH=$JAVA_HOME/bin:$PATH

COPY --from=build /myjre $JAVA_HOME

WORKDIR /app

COPY --from=build /app/target/hello-world-0.0.1-SNAPSHOT.jar /app/
