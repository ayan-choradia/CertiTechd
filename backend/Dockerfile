FROM python:3.10.6
SHELL ["/bin/bash", "-c"]
# Install ODBC dependencies
RUN apt-get update && apt-get install -y \
    unixodbc \
    unixodbc-dev \
    freetds-dev \
    tdsodbc
# Install the MSSQL ODBC driver
RUN apt-get install -y gnupg2 curl
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql18
WORKDIR /app
ENV PYTHONUNBUFFERED=1
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
# Set the environment variable for ODBC driver
ENV ODBCINI=/etc/odbc.ini
ENV ODBCSYSINI=/etc
COPY . /app
EXPOSE 8000
ENV PYTHONPATH=/app
