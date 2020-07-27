import os
import requests
from tqdm import tqdm


def download_file(url, path_out=''):
    local_filename = url.split('/')[-1]
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        if path_out and not path_out.isspace():
            os.makedirs(path_out, exist_ok=True)
        with tqdm.wrapattr(open(path_out + local_filename, "wb"), "write", miniters=1,
                           total=int(r.headers.get('content-length', 0)),
                           desc=local_filename) as fout:
            for chunk in r.iter_content(chunk_size=4096):
                fout.write(chunk)

        fout.flush()

    local_file_path = path_out + local_filename

    return local_filename, local_file_path
