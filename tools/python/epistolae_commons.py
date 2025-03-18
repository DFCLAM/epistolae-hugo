import pathlib

epistolae_hugo_path = pathlib.Path(__file__).parent.parent.parent

def read_hugo_front_matter(path: pathlib.Path):
    for line in path:
        if line.startswith('---'):
            for line in path:
                if line.startswith('---'):
                    return
                yield line

