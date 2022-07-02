# Demo: BinderLite

Preliminary proof-of-concept of building JupyterLite distributions for Binder repositories.

## Build container

docker build -t binderlite .

## Build repository and serve on port 8000

```
docker run --rm -p 8000:8000 binderlite ./build.py https://gist.github.com/manics/626496ed5c9b93e694ac006181e331ec --server
```

## Build repository in a local mounted `build` directory

```
docker run --rm -p 8000:8000 -v $PWD/build:/home/mambauser/build binderlite ./build.py https://gist.github.com/manics/626496ed5c9b93e694ac006181e331ec
```

Serve locally (port 8000):

```
python -m http.server -d build/jl
```
