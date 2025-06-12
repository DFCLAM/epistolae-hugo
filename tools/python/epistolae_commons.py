import pathlib

epistolae_hugo_path = pathlib.Path(__file__).parent.parent.parent

def read_hugo_front_matter(path: pathlib.Path):
    """Generator function that extract the Hugo's front matter line by line

    The generator iterates over all the lines included
    between the '---' separators. The separators itself
    are not included.

    Parameters
    ----------
    path : pathlib.Path
        the path of the hugo file containing a front matter
    """
    for line in path:
        if line.startswith('---'):
            for line in path:
                if line.startswith('---'):
                    return
                yield line

