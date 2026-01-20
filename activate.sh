# export FLASK_DB_TYPE="postgresql"
# export FLASK_DB_DRIVER="psycopg2"
# export FLASK_DB_SERVER="localhost"
# export FLASK_DB_PORT=5432
export FLASK_DB_TYPE="mysql"
export FLASK_DB_DRIVER="mysqldb"
export FLASK_DB_SERVER="localhost"
export FLASK_DB_PORT=3306
export FLASK_DB_NAME="smges"
export FLASK_DB_USER="smges"
export FLASK_DB_PASS="smges"
#export FLASK_SESSION_TIMEOUT=900
export FLASK_DEBUG="True"
export FLASK_SECRET_KEY="SX65lpPefu5gr3Z5dYR-JkJMpX1Bsh1Ecf6kGJdMOUURymkuJ-rxRcjaPTXQaL9brfUV-pIuesCGyyRlBTM2gA"

# Initialize flask migrate
flask db init 
flask db migrate -m "Initial model"
flask db upgrade
python3 entrypoint.py
