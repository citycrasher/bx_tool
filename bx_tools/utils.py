from django.core.files.storage import FileSystemStorage

def store_file_from_ajax(file):
    fs = FileSystemStorage()
    file_name = fs.save(file.name, file)
    # file_url = fs.url(file_name)
    # Read the file content
    with fs.open(file_name) as f:
        file_content = f.read().decode('utf-8')
    return file_content.split()

def get_urls_from_file(file):
    file_content = file.read().decode('utf-8')
    return file_content.split()