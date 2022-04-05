FROM python:3.9-slim-buster as backend

# Install opencv dependencies
RUN apt-get update \
&& apt-get install libgl1 -y \
&& rm -rf /var/lib/apt/lists*

# Copy over python dependencies
COPY requirements.txt /tmp/requirements.txt

# Install required python packages
RUN python -m venv /opt/venv \
&& /opt/venv/bin/pip install -r /tmp/requirements.txt \
&& /opt/venv/bin/pip install gunicorn

# Set Pythonpath to project root
ENV PATH="/opt/venv/bin:${PATH}" \
 PYTHONPATH=/opt/app \
 DIRECTORY_TO_WATCH=/tmp/stranger_danger

# Copy over python source code
COPY . /opt/app/stranger_danger

# Change working directory
WORKDIR /opt/app/stranger_danger/api/app

CMD ["gunicorn", "main:app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
