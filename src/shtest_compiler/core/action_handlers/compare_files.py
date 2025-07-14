import os

def handle(context, params):
    """
    Action handler: Compares two files for equality.
    Expects params to have 'file1' and 'file2' keys.
    """
    file1 = params.get("file1")
    file2 = params.get("file2")
    if not file1 or not file2:
        return {"identical": False, "reason": "Missing file paths"}
    if not os.path.isfile(file1) or not os.path.isfile(file2):
        return {"identical": False, "reason": "One or both files do not exist"}
    with open(file1, "rb") as f1, open(file2, "rb") as f2:
        identical = f1.read() == f2.read()
    return {"identical": identical, "file1": file1, "file2": file2} 