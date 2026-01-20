FROM python:3.15-rc-alpine

# upgrade pip
RUN pip install --upgrade pip

# get curl for healthchecks
RUN apk add --no-cache curl bash mariadb-client mariadb-connector-c-dev gcc g++ musl-dev libpq-dev

# permissions and nonroot user for tightened security
RUN adduser -D nonroot
RUN mkdir /home/app/ && chown -R nonroot:nonroot /home/app
RUN mkdir -p /var/log/flask-app && touch /var/log/flask-app/flask-app.err.log && touch /var/log/flask-app/flask-app.out.log
RUN chown -R nonroot:nonroot /var/log/flask-app
WORKDIR /home/app
USER nonroot

# copy all the files to the container
COPY --chown=nonroot:nonroot ./entrypoint.py /home/app
COPY --chown=nonroot:nonroot ./app /home/app/app
COPY --chown=nonroot:nonroot ./docker-entrypoint.sh /home/app
RUN chmod 755 /home/app/docker-entrypoint.sh
COPY --chown=nonroot:nonroot ./requirements.txt /home/app

# venv
ENV VIRTUAL_ENV=/home/app/venv

# python setup
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install -r requirements.txt

# define the port number the container should expose
EXPOSE 5000

# configure the container to run in an executed manner
ENTRYPOINT ["/home/app/docker-entrypoint.sh"]
CMD ["gunicorn","-w", "3", "-t","60", "-b", "0.0.0.0:5000", "--access-logfile", "'-'", "entrypoint:app"  ]
