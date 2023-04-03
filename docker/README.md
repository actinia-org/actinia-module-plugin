# actinia-module-plugin

You can run actinia-module-plugin as actinia-core plugin.
To run actinia-module-plugin with actinia-core, see [local dev setup with docker](https://github.com/mundialis/actinia_core/blob/master/docker/README.md#Local-dev-setup-with-docker)
Mind that it needs to be registered in the actinia-core config under API.plugins

## DEV notes

__test endpoints__
```bash
ACTINIA_URL="http://127.0.0.1:8088"
ACTINIA_VERSION="v3"
${ACTINIA_URL}/api/${ACTINIA_VERSION}/grass_modules
${ACTINIA_URL}/api/${ACTINIA_VERSION}/grass_modules/d.barscale
${ACTINIA_URL}/api/${ACTINIA_VERSION}/grass_modules/d.barscale3

${ACTINIA_URL}/api/${ACTINIA_VERSION}/actinia_modules
${ACTINIA_URL}/api/${ACTINIA_VERSION}/actinia_modules/vector_area

${ACTINIA_URL}/api/${ACTINIA_VERSION}/modules
${ACTINIA_URL}/api/${ACTINIA_VERSION}/modules/d.barscale
${ACTINIA_URL}/api/${ACTINIA_VERSION}/modules/vector_area
${ACTINIA_URL}/api/${ACTINIA_VERSION}/modules/vector_area5

${ACTINIA_URL}/api/${ACTINIA_VERSION}/swagger.json

```

## Create API docs
```bash
wget -O /tmp/actinia-module.json ${ACTINIA_URL}/api/${ACTINIA_VERSION}/swagger.json
```
Run spectacle docker image to generate the HTML documentation
```bash
docker run -v /tmp:/tmp -t sourcey/spectacle \
  spectacle /tmp/actinia-module.json -t /tmp

# or with local installation (npm install -g spectacle-docs, python2 required)
cd actinia_module_plugin/static
spectacle /tmp/actinia-module.json -t .

# to build all in one file:
spectacle -1 /tmp/actinia-module.json -t .
```
beautify css
```bash
sed -i 's+<link rel="stylesheet" href="stylesheets/spectacle.min.css" />+<link rel="stylesheet" href="stylesheets/spectacle.min.css" />\n    <link rel="stylesheet" href="stylesheets/actinia.css" />+g' index.html
```


## Copy&Paste one-liner
```bash
wget -O /tmp/actinia-module.json ${ACTINIA_URL}/api/${ACTINIA_VERSION}/swagger.json && spectacle /tmp/actinia-module.json -t . && mv public/index.html index.html && rm -r public && sed -i 's+<link rel="stylesheet" href="stylesheets/spectacle.min.css" />+<link rel="stylesheet" href="stylesheets/spectacle.min.css" />\n    <link rel="stylesheet" href="stylesheets/actinia.css" />+g' index.html
```
