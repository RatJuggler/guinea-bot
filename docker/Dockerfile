# Create the guinea-bot Python application image.
FROM python:3.7-alpine3.11 AS guinea-bot

ARG BUILD_TAG=local
LABEL build_tag=${BUILD_TAG}
LABEL description="guinea-bot - Python Application"

# Run the guinea-bot with metrics.
CMD ["guineabot", "-h", "/src", "-m"]
HEALTHCHECK --interval=1h --timeout=30s --start-period=60s --retries=3 \
    CMD ["guineabot", "-t"]

EXPOSE 8000

# Create a folder to install the application from.
WORKDIR /src

# Copy and install the application.
COPY . .
RUN pip3 install --no-cache-dir -U .
