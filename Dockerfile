# CrossSlice: everything the analysis needs (git, GNU Global, clangd, gcc, Java + GumTree, Python).
#   docker build -t crossslice .
#   docker run --rm -p 8000:8000 crossslice                     # explorer on the bundled example
# On your own checkout (mounted at /repo, the working directory; caches in a named volume;
# running as your user so nothing in the checkout ends up owned by root):
#   alias crossslice='docker run --rm -i -u "$(id -u):$(id -g)" \
#       -v "$PWD:/repo" -v crossslice-cache:/cache crossslice'
#   crossslice enrich                  # commit context of HEAD
#   crossslice context src/foo.c:120   # code context at a line
#   crossslice mcp                     # stdio MCP server for agents
#   docker run --rm -p 8000:8000 -u "$(id -u):$(id -g)" -v "$PWD:/repo" \
#       -v crossslice-cache:/cache crossslice explore      # http://127.0.0.1:8000/
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
        git global clangd gcc libc6-dev openjdk-21-jre-headless curl ca-certificates unzip \
    && rm -rf /var/lib/apt/lists/*

# GumTree 4.0.0-beta3 (AST differencing)
RUN curl -sSL -o /tmp/gumtree.zip \
        https://github.com/GumTreeDiff/gumtree/releases/download/v4.0.0-beta3/gumtree-4.0.0-beta3.zip \
    && mkdir -p /opt/gumtree && unzip -q /tmp/gumtree.zip -d /opt/gumtree && rm /tmp/gumtree.zip
ENV GUMTREE_PATH=/opt/gumtree/gumtree-4.0.0-beta3/bin/gumtree

# Python environment via uv (interpreter outside /root, so any uid can run it)
COPY --from=ghcr.io/astral-sh/uv:0.11.6 /uv /usr/local/bin/uv
ENV UV_PYTHON_INSTALL_DIR=/opt/python
WORKDIR /app
COPY pyproject.toml uv.lock .python-version README.md ./
COPY crossslice ./crossslice
RUN uv sync --frozen --no-dev
ENV PATH=/app/.venv/bin:$PATH
COPY examples ./examples

# mounted repositories are owned by another uid; any uid may run the image (-u)
RUN git config --system --add safe.directory '*' \
    && mkdir -p /cache /repo && chmod 1777 /cache /repo
ENV CROSSSLICE_CACHE_DIR=/cache \
    CROSSSLICE_HOST=0.0.0.0 \
    HOME=/tmp

WORKDIR /repo
EXPOSE 8000
ENTRYPOINT ["crossslice"]
CMD ["explore", "-C", "/app/examples/taskrunner", "--focus", "sched_submit"]
