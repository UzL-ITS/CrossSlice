#!/usr/bin/env bash
# Installs the external tools required by the context-enrichment pipeline.
# Tested on CentOS Stream 9 / RHEL 9. Run as root (or with sudo).
#
# Tools:
#   - GumTree 4.0.0-beta3 (AST diff)        -> /opt/gumtree, env GUMTREE_PATH
#   - GNU global 6.6.14 (gtags/global)      -> /usr/local/bin
#   - clangd (LSP)                          -> /usr/bin/clangd
#   - Java 21 (GumTree runtime)
set -euo pipefail

GUMTREE_VERSION=4.0.0-beta3
GLOBAL_VERSION=6.6.14
WORKDIR=$(mktemp -d)
trap 'rm -rf "$WORKDIR"' EXIT

echo "==> Installing distro packages (clangd, Java, build deps)"
dnf install -y clang-tools-extra java-21-openjdk-headless gcc make ncurses-devel unzip curl git

echo "==> Building GNU global ${GLOBAL_VERSION} from source (not packaged for EL9)"
if ! command -v gtags >/dev/null; then
    cd "$WORKDIR"
    curl -sL -O "https://ftp.gnu.org/gnu/global/global-${GLOBAL_VERSION}.tar.gz"
    tar xzf "global-${GLOBAL_VERSION}.tar.gz"
    cd "global-${GLOBAL_VERSION}"
    ./configure --prefix=/usr/local
    make -j"$(nproc)"
    make install
fi
gtags --version | head -1

echo "==> Installing GumTree ${GUMTREE_VERSION}"
if [ ! -x "/opt/gumtree/gumtree-${GUMTREE_VERSION}/bin/gumtree" ]; then
    cd "$WORKDIR"
    curl -sL -o gumtree.zip \
        "https://github.com/GumTreeDiff/gumtree/releases/download/v${GUMTREE_VERSION}/gumtree-${GUMTREE_VERSION}.zip"
    mkdir -p /opt/gumtree
    unzip -qo gumtree.zip -d /opt/gumtree
fi
"/opt/gumtree/gumtree-${GUMTREE_VERSION}/bin/gumtree" --help >/dev/null

cat <<EOF

Done. Add to your environment (e.g. ~/.bashrc):

    export GUMTREE_PATH=/opt/gumtree/gumtree-${GUMTREE_VERSION}/bin/gumtree

EOF
