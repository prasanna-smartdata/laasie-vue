FROM python:3.9-slim

ENV PORT 8080
ENV APP_HOME /api

WORKDIR $APP_HOME
# Copy local code to the container image.
COPY . ./

# Install production dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Reset the working dir to / so that gunicorn can
# find the app factory method inside the api
# package.
WORKDIR /

# Run the web service on container startup.
# Timeout is set to 0 to disable the timeouts
# of the workers to allow AWS to handle
# instance scaling.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 4 --timeout 0 --error-logfile "-" --access-logfile "-" "api:create_app()"
