from shtest_compiler.utils.canonicalization import get_canonical_phrase_and_opposite
import os
import time
class DateModifiedValidation:
    def __init__(self, groups, scope="global"):
        self.file = groups[0] if len(groups) > 0 else None
        self.date = groups[1] if len(groups) > 1 else None
        self.scope = scope
    def to_shell(self, varname="result", last_file_var=None):
        file_path = self.file if self.file else last_file_var
        phrase, opposite = get_canonical_phrase_and_opposite("date_modified", plugin_name="file")
        if not file_path or not self.date:
            return [f"echo 'ERROR: Missing file or date for date_modified validation'"]
        return [
            f"expected='{phrase}'",
            f"if [ -f '{file_path}' ]; then file_date=$(date -r '{file_path}' +%Y%m%d%H%M); if [ \"$file_date\" = '{self.date}' ]; then actual='{phrase}'; else actual='{opposite}'; fi; else actual='{opposite}'; fi",
            f"{varname}=1; [ \"$actual\" = \"$expected\" ] || {varname}=0"
        ]
def handle(groups, scope="global"):
    return DateModifiedValidation(groups, scope) 