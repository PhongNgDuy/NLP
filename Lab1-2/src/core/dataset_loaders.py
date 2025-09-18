def load_raw_text_data(filepath: str) -> str:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = f.read()
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"Không tìm thấy file: {filepath}")
    except Exception as e:
        raise RuntimeError(f"Lỗi khi load dataset: {e}")
