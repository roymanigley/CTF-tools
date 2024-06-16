import argparse
import mimetypes
import os
import requests


def upload(*, url, file, mime_type):
    with open(file, 'rb') as f:
        response = requests.post(
            url=url,
            files={
                'file': (os.path.basename(f.name), f, mime_type)
            }
        )
        print(response.status_code)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-u', '--url',
        required=True, help='the url for thr filr upload'
    )
    parser.add_argument(
        '-f', '--file',
        required=True, help='the file to upload'
    )
    parser.add_argument(
        '-m', '--mime-type',
        help='the mime type for the uploaded file'
    )

    args = parser.parse_args()
    if not os.path.exists(args.file) or not os.path.isfile(args.file):
        print(f'[!] invalid file: {args.file}')
        exit(1)
    if args.mime_type is None:
        mime_type, _ = mimetypes.guess_type(args.file)
        if mime_type:
            args.mime_type = mime_type
        else:
            args.mime_type = mimetypes.types_map['.txt']
    
    upload(**args.__dict__)
