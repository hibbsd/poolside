import psycopg2
import psycopg2.extras
from flask import request, jsonify
from .db import get_connection


def register_routes(app):

    # -------------------------------------------------------------------------
    # POST /write
    # Expects JSON body: {"key": "my-key", "value": "hello world"}
    # -------------------------------------------------------------------------

    @app.route("/write", methods=["POST"])
    def write_string():
        data = request.get_json()

        if not data or "key" not in data or "value" not in data:
            return jsonify({"error": "Request body must include 'key' and 'value'"}), 400

        key   = data["key"]
        value = data["value"]

        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO string_store (key, value)
                        VALUES (%s, %s)
                        ON CONFLICT (key)
                        DO UPDATE SET value      = EXCLUDED.value,
                                      created_at = NOW();
                    """, (key, value))
                conn.commit()
        except psycopg2.Error as e:
            return jsonify({"error": f"Database write failed: {e}"}), 500

        return jsonify({"success": True, "key": key}), 200


    # -------------------------------------------------------------------------
    # GET /retrieve/<key>
    # Returns the stored value for the given key
    # -------------------------------------------------------------------------

    @app.route("/retrieve/<string:key>", methods=["GET"])
    def read_string(key):
        try:
            with get_connection() as conn:
                with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                    cur.execute(
                        "SELECT value FROM string_store WHERE key = %s;",
                        (key,)
                    )
                    row = cur.fetchone()
        except psycopg2.Error as e:
            return jsonify({"error": f"Database read failed: {e}"}), 500

        if row is None:
            return jsonify({"error": f"Key '{key}' not found."}), 404

        return jsonify({"key": key, "value": row["value"]}), 200