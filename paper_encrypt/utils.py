def get_file_ext(file_path):
    if file_path.endswith('.pdf'):
        return 'pdf'

    if file_path.endswith('png') or file_path.endswith('jpg') or file_path.endswith('jpeg'):
        return 'img'

    if file_path.endswith('.txt'):
        return 'txt'

    return None
