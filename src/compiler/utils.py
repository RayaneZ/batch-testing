def shell_condition(success_val, fail_val, expected_val):
    return [
        f"if [ $last_ret -eq 0 ]; then actual=\"{success_val}\"; else actual=\"{fail_val}\"; fi",
        f"expected=\"{expected_val}\""
    ]