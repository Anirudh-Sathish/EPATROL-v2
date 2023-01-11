from waitress import serve
import app2
serve(app2.app, host='0.0.0.0', port=8080)