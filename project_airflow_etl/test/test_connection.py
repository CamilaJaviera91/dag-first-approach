# pyright: reportMissingImports=false

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from unittest.mock import patch, MagicMock
from etl_modules.connection import get_connection

@patch("etl_modules.connection.psycopg2.connect")
@patch("etl_modules.connection.os.getenv")
def test_get_connection_success(mock_getenv, mock_connect):
    # Simular valores de entorno
    env_vars = {
        "DB_HOST": "localhost",
        "DB_PORT": "5432",
        "DB_NAME": "test_db",
        "DB_USER": "test_user",
        "DB_PASSWORD": "test_pass",
        "DB_SCHEMA": "public"
    }
    mock_getenv.side_effect = lambda key: env_vars.get(key)

    # Simular conexión y cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_conn

    conn, cur = get_connection()

    assert conn is not None
    assert cur is not None
    mock_connect.assert_called_once_with(
        host="localhost",
        port="5432",
        dbname="test_db",
        user="test_user",
        password="test_pass"
    )
    mock_cursor.execute.assert_called_once_with("SET search_path TO public;")

@patch("etl_modules.connection.psycopg2.connect", side_effect=Exception("Connection failed"))
@patch("etl_modules.connection.os.getenv", return_value="fake_value")
def test_get_connection_failure(mock_getenv, mock_connect):
    conn, cur = get_connection()
    assert conn is None
    assert cur is None