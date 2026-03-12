import time
import shutil
from pathlib import Path

import requests
from invoke.tasks import task

DOCKER_CONTAINER = "schemathesis-library-workshop"
DOCKER_IMAGE = "schemathesis-library-workshop-test-app"
DOCKER_APP_URL = "http://127.0.0.1"
ROOT_DIR = Path(__file__).parent
ATEST_OUTPUT_DIR = ROOT_DIR / "atest" / "output"


@task
def stop(ctx):
    """Stop and remove the test app container+image."""
    try:
        ctx.run(f"docker stop {DOCKER_CONTAINER}")
    except Exception as error:
        print(f"Error stopping container: {error}")
    try:
        ctx.run(f"docker rm {DOCKER_CONTAINER}")
    except Exception as error:
        print(f"Error removing container: {error}")
    try:
        ctx.run(f"docker image rm {DOCKER_IMAGE}")
    except Exception as error:
        print(f"Error removing image: {error}")


@task(pre=[stop])
def start_app(ctx):
    """Build docker image and start the test app."""
    ctx.run(f"docker build -t {DOCKER_IMAGE} .")
    ctx.run(f"docker run -d --name {DOCKER_CONTAINER} -p 80:80 {DOCKER_IMAGE}")
    try_count = 120
    for i in range(try_count):
        time.sleep(1)
        try:
            response = requests.get(DOCKER_APP_URL)
            if response.status_code == 200:
                print(f"Test app is running: {DOCKER_APP_URL}")
                break
            time.sleep(1)
        except requests.ConnectionError as error:
            print(f"Connection error: {error}")
        if i == try_count - 1:
            raise RuntimeError("Test app did not start in time")


@task
def lint(ctx):
    """Run linters."""
    print("Run ruff format")
    ctx.run("uv run ruff format .")
    print("Run ruff check")
    ctx.run("uv run ruff check --fix  .")
    print("Run mypy")
    ctx.run("uv run mypy .")
    print("Run RoboTidy")
    ctx.run("uv run robocop format")


@task(pre=[start_app])
def atest(ctx, suite: str | None = None):
    """Run acceptance tests."""
    args = [
        "uv",
        "run",
        "robot",
        "--loglevel",
        "DEBUG:INFO",
        "--outputdir",
        ATEST_OUTPUT_DIR.as_posix(),
    ]
    if suite:
        args.extend(["--suite", suite])
    args.append("atest")
    shutil.rmtree(ATEST_OUTPUT_DIR, ignore_errors=True)
    ATEST_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Running {args}")
    ctx.run(" ".join(args))
