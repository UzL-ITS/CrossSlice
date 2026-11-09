"""CrossSlice: demand-driven inter-procedural code context for commits and repositories.

Public entry points:
    from crossslice import RepoGraph      # on-demand repository graph (expand / neighborhood / update)
    from crossslice import enrich_commit  # intra + cross-function context for one commit
CLI: `crossslice --help`.
"""
__version__ = "0.1.0"
__all__ = ["RepoGraph", "enrich_commit", "__version__"]


def __getattr__(name):  # lazy: importing the package must stay cheap and side-effect free
    if name == "RepoGraph":
        from crossslice.cross.graph import RepoGraph
        return RepoGraph
    if name == "enrich_commit":
        from crossslice.commit import enrich_commit
        return enrich_commit
    raise AttributeError(name)
