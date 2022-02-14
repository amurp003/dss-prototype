from flask import Flask, request

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    SimpleSpanProcessor,
)
from opentelemetry.exporter.zipkin.json import ZipkinExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
PORT = 8000
MESSAGE = "Hello, world!\n"

app = Flask(__name__)

# create a ZipkinExporter
zipkin_exporter = ZipkinExporter(
)

trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(
    SimpleSpanProcessor(zipkin_exporter)
)


FlaskInstrumentor().instrument_app(app)


@app.route("/")
def root():
    result = MESSAGE.encode("utf-8")
    return result

if __name__ == "__main__":
    app.run(port=PORT, debug=True, use_reloader=False)