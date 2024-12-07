from flask import Flask, render_template
import os
import socket
import pymysql
from sqlalchemy import create_engine, text
from dotenv import load_dotenv


app = Flask(__name__)

# Install pymysql as MySQLdb
pymysql.install_as_MySQLdb()

# Access environment variables
load_dotenv(".env")

# Load sensitive information from environment variables
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')  # Make sure DB_PORT is set
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

# Debug: Print the values to check if they are loaded correctly
print(f"DB_USER: {DB_USER}, DB_PASSWORD: {DB_PASSWORD}, DB_HOST: {DB_HOST}, DB_NAME: {DB_NAME}")

# Build the database connection URL
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:25060/{DB_NAME}"

print(f"Final DATABASE_URL: {DATABASE_URL}")

# SSL Configuration (only CA certificate needed)
ssl_args = {
    'ssl': {
        'ssl_ca': '/private/ca-certificate.crt',  # Path to the CA certificate
    }
}

# Initialize the SQLAlchemy engine
engine = create_engine(DATABASE_URL, connect_args=ssl_args)

@app.route("/")
def hello():
    name = os.getenv("NAME", "Cody")
    # Get the hostname of the machine
    hostname = socket.gethostname()
    podname = os.getenv("POD NAME", "Unknown Pod")
    nodename = os.getenv("NODE_NAME", "Unknown Node")

    # Pass data to the template
    return render_template("home.html", name=name, hostname=hostname ,podname=podname, nodename=nodename)

@app.route("/database")
def show_db_connection():
    db_host = os.getenv("DB_HOST", "Unknown Host")
    db_region = os.getenv("DO_REGION", "Unknown Region")

    try:
        with engine.connect() as connection:
            # Query to fetch the first row's name and content fields
            result = connection.execute(text("SELECT name, content FROM interview_data LIMIT 1")).fetchone()

            # Ensure the query returned a result
            if result:
                name, content = result[0], result[1]
                versionQuery = connection.execute(text("SELECT VERSION();")).fetchone()
                return render_template("database.html", success=True, name=name, content=content, db_host=db_host, db_region=db_region, versionQuery=versionQuery)
            else:
                return render_template("database.html", success=False, error="The table is empty.")
    except Exception as e:
        return render_template("database.html", success=False, error=str(e))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)

