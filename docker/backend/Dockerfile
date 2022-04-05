FROM python:3.9-slim-buster as backend

# Install opencv dependencies
RUN apt-get update \
&& apt-get install libgl1 make -y \
&& rm -rf /var/lib/apt/lists*

# Copy over python dependencies
COPY stranger_danger/requirements.txt /tmp/requirements.txt

# Install required python packages
RUN python -m venv /opt/venv \
&& /opt/venv/bin/pip install -r /tmp/requirements.txt \
&& /opt/venv/bin/pip install gunicorn

# Set Pythonpath to project root
ENV PATH="/opt/venv/bin:${PATH}" \
 PYTHONPATH=/opt/app \
 DIRECTORY_TO_WATCH=/tmp/stranger_danger

# Change working directory
WORKDIR /opt/app

# Copy over python source code
COPY ./stranger_danger ./stranger_danger

CMD ["gunicorn", "--chdir", "/opt/app/stranger_danger/api/app", "main:app", \
      "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker",\
      "--bind", "0.0.0.0:8000"]


# Create dedicated image for tests
FROM backend as tests

# Copy over dev requirements
COPY stranger_danger/requirements-dev.txt /tmp/requirements-dev.txt

# Install dev requirements
RUN /opt/venv/bin/pip install -r /tmp/requirements-dev.txt

# Copy over tests
COPY . .
