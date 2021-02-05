# Create the guinea-bot Python application image.
FROM python:3.7-alpine3.11 AS guinea-bot

ARG BUILD_TAG=local
LABEL build_tag=${BUILD_TAG}
LABEL description="guinea-bot - Python Application"

# Create a folder to install the application from.
WORKDIR /src

# Copy and install the application.
COPY . .
RUN pip3 install -U .

# Run the guinea-bot.
CMD ["guineabot", "-h", "/src"]
