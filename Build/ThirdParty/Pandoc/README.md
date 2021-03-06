# Build a Pandoc image complete with texlive

```
docker build -t pandoc .
```
(Needs to load a 5.5GB image from docker hub.)
You also get the latex distribution as well.

# To generate the report in PDF format

```bash
(cd ~/DARPA/ALIGN.wiki/2019-Q1-Quarterly-Report-from-Intel/; tar cvfh - .) | docker run --rm --mount source=wikiVol,target=/wiki -i ubuntu bash -c "cd /wiki && tar xvf -"
docker run --rm --mount source=wikiVol,target=/wiki -it pandoc bash -c "cd /wiki && pandoc 2019-Q1-Quarterly-Report-from-Intel.md -f gfm -o x.pdf"
docker run --rm --mount source=wikiVol,target=/wiki ubuntu bash -c "cd /wiki && tar cvf - x.pdf" | tar xvf - 
```

# To resize an image
It seems that the `<img src="images/foo.png" width="300" >` technique for specifying image width in GitHub Flavored markdown does not work with Pandoc.
So instead, resize the images up front using imagemagick's `convert`.
Here is one way to preserve the aspect ratio and make the image height be 300 pixels:
```bash
convert device-schematic.png -resize x300 device-schematic_x300.png
```
