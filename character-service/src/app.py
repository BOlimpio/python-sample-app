from flask import Flask, jsonify, request
import logging.config
from sqlalchemy import exc
import configparser
import debugpy
import os
from db import db
from Character import Character


# Configure the logging package from the logging ini file; defined as an environment variable
logging.config.fileConfig('/config/logging.ini',
                          disable_existing_loggers=False)

# Get a logger for our module
log = logging.getLogger(__name__)

# Setup debugger
debug = os.getenv('DEBUG', 'False')
if debug == 'True':
    debugpy.listen(("0.0.0.0", 5678))
    log.info('Started debugger on port 5678')


def get_database_url():
    """
    Loads the database configuration from the db.ini file and returns
    a database URL.
    :return: A database URL, built from values in the db.ini file
    """
    # Load our database configuration
    config = configparser.ConfigParser()
    config.read('/config/db.ini')
    database_configuration = config['mysql']
    host = database_configuration['host']
    username = database_configuration['username']
    db_password = open('/run/secrets/db_password')
    password = db_password.read()
    database = database_configuration['database']
    database_url = f'mysql://{username}:{password}@{host}/{database}'
    log.info(f'Connecting to database: {database_url}')
    return database_url


# Configure Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = get_database_url()
db.init_app(app)


# curl -v http://localhost:5000/characters
@app.route('/characters')
def get_characters():
    log.debug('GET /characters')
    try:
        characters = [character.json for character in Character.find_all()]
        return jsonify(characters)
    except exc.SQLAlchemyError:
        log.exception('An exception occurred while retrieving all characters')
        return 'An exception occurred while retrieving all characters', 500


# curl -v http://localhost:5000/character/1
@app.route('/character/<int:id>')
def get_character(id):
    log.debug(f'GET /character/{id}')

    try:
        character = Character.find_by_id(id)
        if character:
            return jsonify(character.json)
        log.warning(f'GET /character/{id}: character not found')
        return f'character with id {id} not found', 404
    except exc.SQLAlchemyError:
        log.exception(f'An exception occurred while retrieving character {id}')
        return f'An exception occurred while retrieving character {id}', 500


# curl --header "Content-Type: application/json" --request POST --data '{"name": "character 3"}' -v http://localhost:5000/character
@app.route('/character', methods=['POST'])
def post_character():

    # Retrieve the character from the request body
    request_character = request.json
    log.debug(f'POST /characters with character: {request_character}')

    # Create a new character
    character = Character(None, request_character['name'],request_character['anime'])

    try:
        # Save the character to the database
        character.save_to_db()

        # Return the jsonified character
        return jsonify(character.json), 201
    except exc.SQLAlchemyError:
        log.exception(
            f'An exception occurred while creating character with name: {character.name}')
        return f'An exception occurred while creating character with name: {character.name}', 500


# curl --header "Content-Type: application/json" --request PUT --data '{"name": "Updated character 2"}' -v http://localhost:5000/character/2
@app.route('/character/<int:id>', methods=['PUT'])
def put_character(id):
    log.debug(f'PUT /character/{id}')
    try:
        existing_character = Character.find_by_id(id)

        if existing_character:
            # Get the request payload
            updated_character = request.json

            existing_character.name = updated_character['name']
            existing_character.anime = updated_character['anime']
            existing_character.save_to_db()

            return jsonify(existing_character.json), 200

        log.warning(f'PUT /character/{id}: Existing character not found')
        return f'character with id {id} not found', 404

    except exc.SQLAlchemyError:
        log.exception(
            f'An exception occurred while updating character with name: {updated_character.name}')
        return f'An exception occurred while updating character with name: {updated_character.name}', 500


# curl --request DELETE -v http://localhost:5000/character/2
@app.route('/character/<int:id>', methods=['DELETE'])
def delete_character(id):
    log.debug(f'DELETE /character/{id}')
    try:
        existing_character = Character.find_by_id(id)
        if existing_character:
            existing_character.delete_from_db()
            return jsonify({
                'message': f'Deleted character with id {id}'
            }), 200

        log.warning(f'DELETE /character/{id}: Existing character not found')
        return f'character with id {id} not found', 404

    except exc.SQLAlchemyError:
        log.exception(
            f'An exception occurred while deleting the character with id: {id}')
        return f'An exception occurred while deleting the character with id: {id}', 500


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
