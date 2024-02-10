FROM python:3.6-slim as base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1


FROM base AS python-deps

# Install pipenv and compilation dependencies
RUN pip install pipenv
RUN apt-get update && apt-get install -y --no-install-recommends gcc
# required for proccessing images
RUN apt-get install -y --no-install-recommends libmagic1 && rm -rf /var/lib/apt/lists/*

# Install python dependencies in /.venv
COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

RUN pip install filemagic

FROM base AS runtime

RUN apt-get update
RUN apt-get install libmagic1 -y --no-install-recommends

# Copy virtual env from python-deps stage
COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

# Create and switch to a new user
RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

# Install application into container
COPY . .

# flask port
EXPOSE 5000

RUN mkdir -p uploads

# Run the application
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]