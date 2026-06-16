from flask import Flask, jsonify


def register_routes(app: Flask) -> None:
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({'status': 'ok', 'message': 'CineRate API is running'})
