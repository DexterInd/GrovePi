# Development Notes

To fire up a development environment for the documentation, you need to build this docker file first
```
docker image build -t dexterind/grovepi-docs .
```

Once you have that, you need to fire up the container. First make sure you are running this from the root of this repository and then run
```
docker container run -v $(pwd):/docs -it --rm -p 80:8000 dexterind/grovepi-docs
```


Enjoy developing and when you're done with it, build the documentation and save the statics in the docs folder.
