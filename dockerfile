FROM python:3.10.1

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# update packages
RUN apt-get update

# Set working directory
WORKDIR /twitter

# copy requirements files
COPY ./requirements.txt /twitter/requirements.txt

# install requirements
RUN pip install -r requirements.txt

# Copy codebase
COPY . /twitter/

# create new user
RUN adduser --disabled-password --gecos '' jerry

# Set user as the owner of directory
RUN chown -R jerry:jerry /twitter

##Set user to be jerry
USER jerry

