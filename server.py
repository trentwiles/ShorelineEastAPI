from waitress import serve
import web

print("🚀 Listening @ localhost:10394")
serve(web.app, host='127.0.0.1', port=10394)