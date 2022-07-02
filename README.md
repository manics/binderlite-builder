# Demo: BinderLite

[![Build](https://github.com/manics/binderlite-builder/actions/workflows/build.yml/badge.svg)](https://github.com/manics/binderlite-builder/actions/workflows/build.yml)

Preliminary proof-of-concept of building JupyterLite distributions for Binder repositories.

This only works with very simple `requirements.txt` files.

## Build container

```
docker build -t binderlite .
```

## Build repository and serve on port 8000

```
docker run --rm -p 8000:8000 binderlite \
    ./build.py https://gist.github.com/manics/626496ed5c9b93e694ac006181e331ec --serve
```

## Build repository in a local mounted `build` directory

```
docker run --rm -v $PWD/build:/home/mambauser/build binderlite \
    ./build.py https://gist.github.com/manics/626496ed5c9b93e694ac006181e331ec
```

Serve locally (port 8000):

```
python -m http.server -d build/jl
```
