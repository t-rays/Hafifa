"""Fatal failures. Callers log these at the boundary that stops the run."""


class DownloadError(Exception):
    """Every chunk for a ticker failed or returned no rows."""


class PipelineError(Exception):
    """One or more ticker fetches failed. The report was not written."""
