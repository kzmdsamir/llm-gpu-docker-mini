from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "Local_GPU_LLM_Inference_PoC_Report.pdf"
NAVY = colors.HexColor("#12355B")
BLUE = colors.HexColor("#1F6FB2")
TEAL = colors.HexColor("#0E7490")
PALE_BLUE = colors.HexColor("#EAF3FA")
PALE_TEAL = colors.HexColor("#E6F4F5")
INK = colors.HexColor("#1F2937")
MUTED = colors.HexColor("#64748B")
LINE = colors.HexColor("#CBD5E1")


def styles():
    base = getSampleStyleSheet()
    return {
        "kicker": ParagraphStyle(
            "Kicker",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8.5,
            leading=10,
            textColor=TEAL,
            spaceAfter=10,
            uppercase=True,
        ),
        "title": ParagraphStyle(
            "Title",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=24,
            leading=28,
            textColor=NAVY,
            alignment=TA_LEFT,
            spaceAfter=7,
        ),
        "subtitle": ParagraphStyle(
            "Subtitle",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=11,
            leading=15,
            textColor=MUTED,
            spaceAfter=18,
        ),
        "h1": ParagraphStyle(
            "Heading1",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=15,
            leading=18,
            textColor=NAVY,
            spaceBefore=4,
            spaceAfter=8,
        ),
        "h2": ParagraphStyle(
            "Heading2",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=14,
            textColor=BLUE,
            spaceBefore=8,
            spaceAfter=5,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9.35,
            leading=13.2,
            textColor=INK,
            spaceAfter=7,
        ),
        "small": ParagraphStyle(
            "Small",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8.1,
            leading=10.5,
            textColor=INK,
            spaceAfter=4,
        ),
        "table": ParagraphStyle(
            "Table",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=7.7,
            leading=9.5,
            textColor=INK,
        ),
        "table_head": ParagraphStyle(
            "TableHead",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=7.4,
            leading=8.7,
            textColor=colors.white,
            alignment=TA_CENTER,
        ),
        "callout": ParagraphStyle(
            "Callout",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=10,
            leading=14,
            textColor=NAVY,
        ),
        "footer": ParagraphStyle(
            "Footer",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=7.5,
            leading=9,
            textColor=MUTED,
        ),
    }


def para(text, style):
    return Paragraph(text, style)


def info_table(style_map):
    values = [
        ("Prepared by", "Kazi Md Samir"),
        ("Email", "kzsamir849@gmail.com"),
        ("Phone", "01884382430"),
        ("Repository", "github.com/kzmdsamir/llm-gpu-docker-mini"),
    ]
    rows = []
    for label, value in values:
        rows.append([para(label, style_map["small"]), para(value, style_map["small"])])
    table = Table(rows, colWidths=[1.15 * inch, 5.3 * inch])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), PALE_BLUE),
                ("BOX", (0, 0), (-1, -1), 0.6, LINE),
                ("INNERGRID", (0, 0), (-1, -1), 0.3, LINE),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 9),
                ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return table


def panel(text, style_map):
    table = Table([[para(text, style_map["callout"])]], colWidths=[6.45 * inch])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), PALE_TEAL),
                ("BOX", (0, 0), (-1, -1), 0.8, TEAL),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )
    return table


def architecture_table(style_map):
    cells = [
        para("<b>Client / benchmark</b><br/>HTTP requests and sweep control", style_map["small"]),
        para("<b>FastAPI container</b><br/>Health, readiness, generation gateway", style_map["small"]),
        para("<b>Host Ollama</b><br/>Model runtime via host.docker.internal", style_map["small"]),
        para("<b>RTX 4060</b><br/>8 GB VRAM inference execution", style_map["small"]),
    ]
    arrows = [para("&#8594;", ParagraphStyle("Arrow", parent=style_map["body"], alignment=TA_CENTER, fontSize=16, textColor=TEAL))]
    row = [cells[0], arrows[0], cells[1], arrows[0], cells[2], arrows[0], cells[3]]
    table = Table([row], colWidths=[1.38 * inch, 0.23 * inch, 1.55 * inch, 0.23 * inch, 1.55 * inch, 0.23 * inch, 1.28 * inch])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, 0), PALE_BLUE),
                ("BACKGROUND", (2, 0), (2, 0), PALE_BLUE),
                ("BACKGROUND", (4, 0), (4, 0), PALE_BLUE),
                ("BACKGROUND", (6, 0), (6, 0), PALE_TEAL),
                ("BOX", (0, 0), (0, 0), 0.6, LINE),
                ("BOX", (2, 0), (2, 0), 0.6, LINE),
                ("BOX", (4, 0), (4, 0), 0.6, LINE),
                ("BOX", (6, 0), (6, 0), 0.6, TEAL),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (1, 0), (5, 0), "CENTER"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 9),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
            ]
        )
    )
    return table


def result_table(style_map):
    header = ["Workers", "Success", "Mean", "P50", "P90", "P99", "Gen tok/s", "Outcome"]
    rows = [
        ["1", "19/20", "45.9 s", "41.0 s", "84.3 s", "93.2 s", "24.7", "Completed; one failure"],
        ["2", "19/20", "95.5 s", "80.2 s", "158.1 s", "175.0 s", "13.3", "Completed; one failure"],
        ["4", "N/A", "-", "-", "-", "-", "-", "Saturated; interrupted"],
    ]
    data = [[para(value, style_map["table_head"]) for value in header]]
    data.extend([[para(value, style_map["table"]) for value in row] for row in rows])
    table = Table(data, colWidths=[0.7 * inch, 0.65 * inch, 0.65 * inch, 0.6 * inch, 0.6 * inch, 0.6 * inch, 0.7 * inch, 1.95 * inch], repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("BACKGROUND", (0, 1), (-1, 1), colors.white),
                ("BACKGROUND", (0, 2), (-1, 2), PALE_BLUE),
                ("BACKGROUND", (0, 3), (-1, 3), colors.HexColor("#FEF3C7")),
                ("GRID", (0, 0), (-1, -1), 0.35, LINE),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (6, -1), "CENTER"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return table


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.4)
    canvas.line(doc.leftMargin, 0.52 * inch, letter[0] - doc.rightMargin, 0.52 * inch)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(doc.leftMargin, 0.33 * inch, "Kazi Md Samir | Local GPU LLM Inference PoC")
    canvas.drawRightString(letter[0] - doc.rightMargin, 0.33 * inch, f"Page {doc.page}")
    canvas.restoreState()


def build():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    style_map = styles()
    document = BaseDocTemplate(
        str(OUTPUT),
        pagesize=letter,
        title="Local GPU-Accelerated LLM Inference PoC",
        author="Kazi Md Samir",
        leftMargin=0.55 * inch,
        rightMargin=0.55 * inch,
        topMargin=0.55 * inch,
        bottomMargin=0.72 * inch,
    )
    frame = Frame(document.leftMargin, document.bottomMargin, document.width, document.height, id="main")
    document.addPageTemplates([PageTemplate(id="report", frames=[frame], onPage=footer)])
    story = []
    story.extend(
        [
            para("AI INFRASTRUCTURE INTERNSHIP PREPARATION", style_map["kicker"]),
            para("Local GPU-Accelerated LLM Inference PoC", style_map["title"]),
            para("Containerized serving, GPU validation, and load benchmarking on an NVIDIA RTX 4060 8 GB", style_map["subtitle"]),
            info_table(style_map),
            Spacer(1, 0.22 * inch),
            panel(
                "Built a reproducible local inference workflow: deploy an API container, validate Docker-to-GPU access, exercise the serving path under load, preserve benchmark evidence, and turn observed limits into a concrete improvement plan.",
                style_map,
            ),
            Spacer(1, 0.2 * inch),
            para("Executive Summary", style_map["h1"]),
            para(
                "This project is a local, GPU-backed inference proof of concept aligned to the Solar GPU PoC AI Infrastructure Internship. It packages a FastAPI gateway in Docker, uses host Ollama as the model-serving runtime, adds health and readiness checks, emits structured JSON logs, and includes smoke tests plus concurrent benchmark automation.",
                style_map["body"],
            ),
            para(
                "The intent is not to claim a production deployment or a solar-powered cluster. The intent is to demonstrate practical systems work: repeatable deployment, GPU verification, controlled measurement, honest interpretation, and well-documented next steps.",
                style_map["body"],
            ),
            para("What Was Delivered", style_map["h2"]),
            para(
                "FastAPI endpoints for liveness, readiness, and generation; environment-driven configuration; structured request logs; Dockerfile and Compose deployment; automated smoke tests; concurrent Python load testing; CSV and JSON result artifacts; and an experiment template for repeatable engineering notes.",
                style_map["body"],
            ),
            para("Project Objective", style_map["h2"]),
            para(
                "Measure how an RTX 4060 8 GB behaves while serving the Ollama model tag qwen3.5:9b at increasing request concurrency, then identify the operational bottlenecks relevant to a larger shared GPU environment.",
                style_map["body"],
            ),
        ]
    )
    story.append(PageBreak())
    story.extend(
        [
            para("System Design and Validation", style_map["h1"]),
            architecture_table(style_map),
            Spacer(1, 0.16 * inch),
            para("Service Design", style_map["h2"]),
            para(
                "The FastAPI container exposes GET /health for application liveness, GET /ready to test upstream Ollama reachability, and POST /generate to forward prompts and return latency, generated token count, generation rate, and a request ID. JSON logs preserve generation start, completion, and upstream failure events.",
                style_map["body"],
            ),
            para("Deployment Decision", style_map["h2"]),
            para(
                "The default Compose path runs Ollama on the host and connects from the container through host.docker.internal. GPU execution therefore occurs in the host Ollama process. The API container has an NVIDIA GPU device request configured, but it is not required while the container only relays requests. GPU allocation becomes required when the model runtime is moved into Docker.",
                style_map["body"],
            ),
            para("Verified Environment", style_map["h2"]),
        ]
    )
    environment = [
        ["Host", "Windows 11 with WSL2 Ubuntu and Docker Desktop"],
        ["CPU / RAM", "AMD Ryzen 7 7700, 8 cores / 32 GB RAM"],
        ["GPU", "NVIDIA GeForce RTX 4060, 8,188 MiB VRAM"],
        ["Driver / Docker", "NVIDIA 596.49 / Docker Engine 28.5.1"],
        ["Serving runtime", "Host Ollama via host.docker.internal:11434"],
        ["Model", "qwen3.5:9b (quantization metadata not recorded)"],
    ]
    env_table = Table([[para(a, style_map["table"]), para(b, style_map["table"])] for a, b in environment], colWidths=[1.35 * inch, 5.1 * inch])
    env_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), PALE_BLUE),
                ("GRID", (0, 0), (-1, -1), 0.35, LINE),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.extend(
        [
            env_table,
            Spacer(1, 0.14 * inch),
            panel(
                "Independent GPU proof: docker run --rm --gpus all nvidia/cuda:12.2.0-base-ubuntu22.04 reported NVIDIA GeForce RTX 4060, driver 596.49, and 8188 MiB VRAM from inside the container.",
                style_map,
            ),
        ]
    )
    story.append(PageBreak())
    story.extend(
        [
            para("Benchmark Evidence and Interpretation", style_map["h1"]),
            para("Method", style_map["h2"]),
            para(
                "A Python ThreadPoolExecutor issued 20 HTTP requests to POST /generate with the prompt Explain Docker in 2 sentences. The benchmark records request latency, returned token count, and the per-request generation rate reported by the API, then writes CSV and JSON artifacts. The initial workload intentionally had no MAX_TOKENS cap.",
                style_map["body"],
            ),
            para("Saved Raw Results", style_map["h2"]),
            result_table(style_map),
            Spacer(1, 0.12 * inch),
            para(
                "The worker-specific JSON summaries are treated as the source of truth. An earlier experiment note reports 20/20 success at two workers, while the saved worker-1 and worker-2 summaries each record 19/20 success. The mismatch is documented as a report-quality issue to correct rather than concealed.",
                style_map["small"],
            ),
            para("Key Findings", style_map["h2"]),
            para(
                "1. GPU-container support is verified independently from application behavior. 2. The 9B model is usable at limited concurrency, but mean latency more than doubles from one to two workers. 3. Tail latency and failure risk increase under concurrent load. 4. The four-worker sweep saturated the system and was interrupted. 5. Unbounded generation was the dominant source of response-time variation.",
                style_map["body"],
            ),
            para("Why the Latency Is High", style_map["h2"]),
            para(
                "Although the prompt asked for two sentences, successful worker-2 requests generated approximately 598 to 3,216 tokens. This test is useful as a stress observation, but it is not a controlled interactive-latency baseline. The next run should cap output at 128 or 256 tokens and include output-token counts in every summary.",
                style_map["body"],
            ),
            para("Metric Discipline", style_map["h2"]),
            para(
                "The reported tokens/s value is a per-request generation-rate observation, not total system throughput. Future reports should add requests/s and total generated tokens divided by full test wall time. With only 19 successful requests, P95 is more useful than P99; percentile calculation should use a nearest-rank method before formal comparison.",
                style_map["body"],
            ),
        ]
    )
    story.append(PageBreak())
    story.extend(
        [
            para("Operational Lessons and Internship Relevance", style_map["h1"]),
            para("Observed Constraints", style_map["h2"]),
            para(
                "The application logs recorded upstream Ollama read timeouts under heavier load. The 180-second timeout protects callers from waiting indefinitely, but it does not provide backpressure. The benchmark CSV also omits exception text for failed rows, and GPU utilization telemetry was observed with nvidia-smi rather than stored as a time series. These are practical improvements, not hidden weaknesses.",
                style_map["body"],
            ),
            para("Immediate Improvement Plan", style_map["h2"]),
            para(
                "Repeat the worker-1 and worker-2 runs with MAX_TOKENS=128 and 256; record model metadata with ollama show; persist error classes in CSV; add queue or concurrency limits; capture GPU memory, utilization, temperature, CPU, and RAM during each run; and compare a smaller model using the same fixed workload.",
                style_map["body"],
            ),
            para("Direct Relevance to the Internship", style_map["h2"]),
        ]
    )
    relevance = [
        ["Internship focus", "Evidence from this project"],
        ["Containerized AI", "Dockerfile, Compose, health checks, host-runtime networking"],
        ["Inference serving", "Ollama-backed FastAPI generation API and readiness checks"],
        ["GPU operations", "Host and CUDA-container GPU validation on RTX 4060"],
        ["Benchmarking", "Concurrent load test, raw CSV/JSON, worker sweep, overload evidence"],
        ["Observability", "Structured request logs, request IDs, nvidia-smi monitoring workflow"],
        ["Automation / docs", "Smoke test, benchmark wrappers, experiment template, repeatable report"],
    ]
    relevance_table = Table(
        [[para(value, style_map["table_head"] if row_index == 0 else style_map["table"]) for value in row] for row_index, row in enumerate(relevance)],
        colWidths=[1.45 * inch, 5.0 * inch],
        repeatRows=1,
    )
    relevance_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                ("BACKGROUND", (0, 2), (-1, 2), PALE_BLUE),
                ("BACKGROUND", (0, 4), (-1, 4), PALE_BLUE),
                ("BACKGROUND", (0, 6), (-1, 6), PALE_BLUE),
                ("GRID", (0, 0), (-1, -1), 0.35, LINE),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.extend(
        [
            relevance_table,
            Spacer(1, 0.15 * inch),
            panel(
                "Portfolio statement: I can take a local AI inference service from deployment through verification and measurement, identify reliability limits honestly, and translate results into the next operational experiment for a larger GPU PoC.",
                style_map,
            ),
            Spacer(1, 0.16 * inch),
            para("Reproduce the Baseline", style_map["h2"]),
            para(
                "ollama list  |  docker compose up --build -d  |  ./scripts/smoke_test.sh  |  nvidia-smi -l 1  |  MAX_WORKERS=1 MAX_TOKENS=256 python scripts/benchmark.py", 
                style_map["small"],
            ),
            para("Source evidence: app/main.py, docker-compose.yml, scripts/benchmark.py, scripts/smoke_test.sh, results/benchmark_results.csv, results/benchmark_summary_workers_1.json, results/benchmark_summary_workers_2.json, and docs/experiment_01_qwen3_5_9b_gpu.md.", style_map["small"]),
        ]
    )
    document.build(story)


if __name__ == "__main__":
    build()
