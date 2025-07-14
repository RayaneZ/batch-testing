import os

def handle(context, params):
    """
    Action handler: Updates the contents of a file.
    Expects params to have 'file' and 'content' keys.
    """
    file_path = params.get("file")
    content = params.get("content")
    if not file_path or content is None:
        return {"updated": False, "reason": "Missing file path or content"}
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return {"updated": True, "file": file_path}
    except Exception as e:
        from shtest_compiler.utils.logger import log_pipeline_error
        import traceback
        log_pipeline_error(f"[ERROR] {type(e).__name__}: {e}\n{traceback.format_exc()}")
        raise 