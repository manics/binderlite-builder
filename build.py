#!/usr/bin/env python
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import http.server
import json
from os.path import realpath
from pathlib import Path
from pkg_resources import parse_requirements
from subprocess import call


def file_stats(path):
    """
    Return the number of files and total size in bytes in a directory (recursive)
    """
    n = 0
    size = 0
    for f in path.rglob("*"):
        if f.is_file():
            n += 1
            size += f.stat().st_size
    return n, size


parser = ArgumentParser(
    description="BinderLite builder", formatter_class=ArgumentDefaultsHelpFormatter
)
parser.add_argument("repo", help="Git repository to build")
parser.add_argument(
    "--builddir", help="Build and output directory", default=realpath("build")
)
parser.add_argument("--serve", help="Serve the build directory", action="store_true")
parser.add_argument("--port", help="Port to serve on", type=int, default=8000)
args = parser.parse_args()

builddir = Path(args.builddir)
builddir.mkdir(parents=True, exist_ok=True)
outputdir = builddir / "jl"

r = call(["git", "clone", "--depth", "1", args.repo, "files"], cwd=builddir)
if r != 0:
    raise RuntimeError(f"Failed to clone repository {args.repo}")

requirements = []
for d in (".", "binder", ".binder"):
    f = builddir / "files" / d / "requirements.txt"
    if f.is_file():
        requirements = [str(r) for r in parse_requirements(f.read_text())]

with Path("jupyter_lite_config.json").open() as f:
    jupyter_lite_config = json.load(f)

if requirements:
    jupyter_lite_config["XeusPythonEnv"]["packages"] = requirements

with (builddir / "jupyter_lite_config.json").open("w") as f:
    json.dump(jupyter_lite_config, f)

r = call(["jupyter", "lite", "build", f"--output-dir={outputdir}"], cwd=builddir)
if r != 0:
    raise RuntimeError("Failed: jupyter lite build")

jl_n, jl_size = file_stats(outputdir)

print("\n**********************************************************************\n")
print(f"{outputdir}: {jl_n} files, {jl_size / 1e6} MB")


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=outputdir, **kwargs)


if args.serve:
    with http.server.ThreadingHTTPServer(("", args.port), Handler) as httpd:
        print(f"serving {outputdir} on port {args.port}")
        httpd.serve_forever()
