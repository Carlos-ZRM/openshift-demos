# Build arguments
ARG BASE_IMAGE=registry.redhat.io/rhel9/python-311:9.7
ARG APP_VERSION=1.0.0
ARG BUILD_DATE
ARG VCS_REF

# Base image
FROM ${BASE_IMAGE}

# Labels for image metadata
LABEL maintainer="your-email@example.com"
LABEL description="Python application running on UBI9"
LABEL version="${APP_VERSION}"
LABEL org.opencontainers.image.created="${BUILD_DATE}"
LABEL org.opencontainers.image.revision="${VCS_REF}"
LABEL org.opencontainers.image.url="https://github.com/your-repo"

# Environment variables
ENV APP_HOME=/opt/app \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set working directory
WORKDIR ${APP_HOME}

USER 0
COPY src .
RUN chown -R 1001:0 ./
RUN yum install nmap -y \
    && yum clean all \
    && rm -rf /var/cache/yum
USER 1001

RUN pip install -r requirements.txt

EXPOSE 5000
EXPOSE 513
EXPOSE 514
EXPOSE 22
EXPOSE 23
EXPOSE 20 21
EXPOSE 135 137 139
EXPOSE 445
EXPOSE 111
EXPOSE 143
EXPOSE 110
EXPOSE 80
EXPOSE 25
EXPOSE 2049

ENTRYPOINT ["python", "app.py"]
