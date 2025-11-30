import logging
import random
import time
from fastapi import FastAPI

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor

# ---------- OTEL SETUP ----------

service_name = "traced-fastapi-service"

resource = Resource(attributes={
    "service.name": service_name,
})

provider = TracerProvider(resource=resource)
trace.set_tracer_provider(provider)

# Exporter points to the OTEL collector in the cluster (we'll override via env)
otlp_exporter = OTLPSpanExporter()

span_processor = BatchSpanProcessor(otlp_exporter)
provider.add_span_processor(span_processor)

tracer = trace.get_tracer(__name__)

# ---------- APP SETUP ----------

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(service_name)

app = FastAPI(title="Traced FastAPI Demo")

# Instrument FastAPI & logging
FastAPIInstrumentor.instrument_app(app)
LoggingInstrumentor().instrument(set_logging_format=True)


@app.get("/health")
async def health():
    logger.info("health endpoint called")
    return {"status": "ok"}


@app.get("/work")
async def do_some_work():
    # example of manual span
    with tracer.start_as_current_span("do_some_work-operation"):
        logger.info("Starting some fake work")
        # simulate DB or external call
        time.sleep(random.uniform(0.1, 0.5))
        logger.info("Finished fake work")
        return {"message": "work done!"}


@app.get("/")
async def root():
    logger.info("root endpoint called")
    return {"message": "Hello from traced FastAPI app"}

