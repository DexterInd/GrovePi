Run
```bash
docker image build -t grovepi/mkdocs-serve .
```
to build the image and then from `/docs` directory of this README run
```
docker container run -it --rm -v $(pwd):/docs -p 80:8000 grovepi/mkdocs-serve
```

Once the container is up and running, you can go to `localhost` in your browser and you'll see the documentation.

To build the documentation, run the following container in the same directory as before:
```
docker container run -it --rm -v $(pwd):/docs 80:8000 grovepi/mkdocs-serve mkdocs build
```
