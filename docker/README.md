# actinia-module-plugin

You can run actinia-module-plugin as actinia-core plugin.
To run actinia-module-plugin with actinia-core, see https://github.com/mundialis/actinia_core/blob/master/docker/README.md#Local-dev-setup-with-docker
Mind that it needs to be registered in the actinia-core config under API.plugins

## DEV notes

__test endpoints__
```
http://127.0.0.1:8088/api/v1/grassmodules
http://127.0.0.1:8088/api/v1/grassmodules/d.barscale
http://127.0.0.1:8088/api/v1/grassmodules/d.barscale3

http://127.0.0.1:8088/api/v1/actiniamodules
http://127.0.0.1:8088/api/v1/actiniamodules/vector_area

http://127.0.0.1:8088/api/v1/modules
http://127.0.0.1:8088/api/v1/modules/d.barscale
http://127.0.0.1:8088/api/v1/modules/vector_area
http://127.0.0.1:8088/api/v1/modules/vector_area5

http://127.0.0.1:8088/api/v1/swagger.json

```
