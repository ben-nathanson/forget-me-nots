def sanitize_mock_path(path: str) -> str:
    return path.replace("/", ".").removesuffix(".py")
