---
title: Synse v2 API Reference

language_tabs:
  - shell
  - python

toc_footers:
  - Vapor IO • Synse Server • v2

search: true
---

# Overview

Synse Server provides a simple JSON API to monitor and control physical and virtual devices, such as
data center and IT equipment. More generally, it provides a uniform interface for back-ends implementing
various protocols, such as RS485 and I2C. The Synse Server API makes it easy to read from and write
to devices, gather device information, and scan for configured devices through a curl-able interface.


# Errors

```json
{
  "http_code": 404,
  "error_id": 4000,
  "description": "device not found",
  "timestamp": "2018-01-24 19:54:37.382551",
  "context": "rack-1\/board-1\/f52d29fecf05a195af13f14c73065252d does not correspond with a known device."
}
```

Synse Server will return a JSON response with 400, 404, or 500 code errors. The returned JSON is used
to provide context around the error. An example of the response JSON for an error is shown here.

In general,

- **400 responses** relate to invalid user input. This can range from invalid JSON, unsupported
  query parameters, or invalid resource types.
- **404 responses** relate to either the specified URL not being valid or the specified
  resource was not found.
- **500 responses** relate to server-side processing errors.

The fields for the error response are:

| Field | Description |
| ----- | ----------- |
| *http_code* | The HTTP code corresponding to the the error (e.g. 400, 404, 500). |
| *error_id* | The Synse Server defined error ID. This is used to identify the type of error. |
| *description* | A short description for the error type, as defined by the `error_id`. |
| *timestamp* | The time at which the error occurred. |
| *context* | Any message associated with the error to provide information on the root cause of the error. |


The currently defined error IDs follow.

| Error ID | Description |
| -------- | ----------- |
| 0 | Unknown Error |
| 3000 | URL not found |
| 3001 | Invalid arguments |
| 3002 | Invalid JSON |
| 3003 | Invalid device type |
| 4000 | Device not found |
| 4001 | Board not found |
| 4002 | Rack not found |
| 4003 | Plugin not found |
| 4004 | Transaction not found |
| 5000 | Failed info command |
| 5001 | Failed read command |
| 5002 | Failed scan command |
| 5003 | Failed transaction command |
| 5004 | Failed write command |
| 5005 | Failed plugin command |
| 6000 | Internal API failure |
| 6500 | Plugin state error |


# Device Types
Devices in Synse Server are all associated with "type" information (For the full set of information
associated with a device, see the [info](#info) endpoint). While the device types are defined by the
plugin which manages the device, common device types in Synse include:

- airflow
- boot_target
- fan
- humidity
- led
- power
- pressure
- system
- temperature


# Endpoints

## Test

```shell
curl "http://host:5000/synse/test"
```

```python
import requests

response = requests.get('http://host:5000/synse/test')
```

> The response JSON would be structured as:

```json
{
  "status": "ok",
  "timestamp": "2018-01-24 19:22:28.425090"
}
```

Test that the endpoint is reachable.

If the endpoint is reachable (e.g. if Synse Server is up and ready), this will return a 200 response
with the described JSON response. If the test endpoint is unreachable or otherwise fails, it will return
a 500 response. The test endpoint does not have any internal dependencies, so a failure would indicate
Synse Server not being up and serving.

<aside class="notice">
    Note that a 500 response from this endpoint would likely <b>not</b> include any JSON context,
    as a 500 here generally means Synse Server is either not yet running or otherwise unreachable.
</aside>

### HTTP Request

`GET http://host:5000/synse/test`

### Response Fields

| Field | Description |
| ----- | ----------- |
| *status* | "ok" if the endpoint returns successfully. |
| *timestamp* | The time at which the status was tested. |



## Version

```shell
curl "http://host:5000/synse/version"
```

```python
import requests

response = requests.get('http://host:5000/synse/version')
```

> The response JSON would be structured as:

```json
{
  "version": "2.1.0",
  "api_version": "v2"
}

```

Get the version info of the Synse Server instance. The API version provided by this endpoint
should be used in subsequent requests.

### HTTP Request

`GET http://host:5000/synse/version`

### Response Fields

| Field | Description |
| ----- | ----------- |
| *version* | The full version (major.minor.micro) of the Synse Server instance. |
| *api_version* | The API version (major.minor) that can be used to construct subsequent API requests. |



## Config

```shell
curl "http://host:5000/synse/v2/config"
```

```python
import requests

response = requests.get('http://host:5000/synse/v2/config')
```

> The response JSON would be structured as:

```json
{
  "logging": "debug",
  "pretty_json": true,
  "locale": "en_US",
  "plugin": {
    "tcp": [
      "emulator-plugin:5001"
    ]
  },
  "cache": {
    "meta": {
      "ttl": 20
    },
    "transaction": {
      "ttl": 300
    }
  },
  "grpc": {
    "timeout": 3
  }
}
```

Get the unified configuration of the Synse Server instance.

This endpoint is added as a convenience to make it easier to determine what configuration Synse Server
is running with. The Synse Server configuration is made up of default, file, environment, and override
configuration components. This endpoint provides the final joined configuration that Synse Server
ultimately runs with.

See the [Configuration Documentation](http://synse-server.readthedocs.io/en/latest/user/configuration.html)
for more information.

### HTTP Request

`GET http://host:5000/synse/v2/config`

### Response

The response to the `config` endpoint is the unified configuration for Synse Server. The
[Configuration Documentation](http://synse-server.readthedocs.io/en/latest/user/configuration.html)
describes the configuration scheme in more detail.


## Capabilities

```shell
curl "http://host:5000/synse/v2/capabilities"
```

```python
import requests

response = requests.get('http://host:5000/synse/v2/capabilities')
```

> The response JSON would be structured as:

```json
[
  {
    "plugin": "vaporio\/emulator-plugin",
    "devices": [
      {
        "kind": "airflow",
        "outputs": [
          "airflow"
        ]
      },
      {
        "kind": "temperature",
        "outputs": [
          "temperature"
        ]
      },
      {
        "kind": "pressure",
        "outputs": [
          "pressure"
        ]
      },
      {
        "kind": "led",
        "outputs": [
          "led.color",
          "led.state"
        ]
      },
      {
        "kind": "humidity",
        "outputs": [
          "humidity",
          "temperature"
        ]
      },
      {
        "kind": "fan",
        "outputs": [
          "fan.speed"
        ]
      }
    ]
  }
]
```

Get a list of device capabilities from all registered plugins. Device capabilities list out
the outputs for each device kind that a plugin is configured to handle. This lets a user known
which device kinds are supported, and for those device kinds, what readings they can expect.

### HTTP Request

`GET http://host:5000/synse/v2/capabilities`

### Response Fields

| Field | Description |
| ----- | ----------- |
| *plugin* | The name of the plugin with the corresponding device kinds/output types. |
| *devices* | A list of device kinds supported by the plugin. |
| *{device}.kind* | The name of the device kind. |
| *{device}.outputs* | A list of the names of the output types that the device kind supports. |


## Plugins

```shell
curl "http://host:5000/synse/v2/plugins"
```

```python
import requests

response = requests.get('http://host:5000/synse/v2/plugins')
```

> The response JSON would be structured as:

```json
[
  {
    "tag": "vaporio\/emulator-plugin",
    "name": "emulator plugin",
    "description": "A plugin with emulated devices and data",
    "maintainer": "vaporio",
    "vcs": "github.com\/vapor-ware\/synse-emulator-plugin",
    "version": {
      "plugin_version": "2.0.0",
      "sdk_version": "1.0.0",
      "build_date": "2018-06-14T16:24:09",
      "git_commit": "13e6478",
      "git_tag": "1.0.2-5-g13e6478",
      "arch": "amd64",
      "os": "linux"
    },
    "network": {
      "protocol": "tcp",
      "address": "emulator-plugin:5001"
    },
    "health": {
      "timestamp": "2018-06-15T20:04:33.4393472Z",
      "status": "ok",
      "message": "",
      "checks": [
        {
          "name": "read buffer health",
          "status": "ok",
          "message": "",
          "timestamp": "2018-06-15T20:04:06.3524458Z",
          "type": "periodic"
        },
        {
          "name": "write buffer health",
          "status": "ok",
          "message": "",
          "timestamp": "2018-06-15T20:04:06.3523946Z",
          "type": "periodic"
        }
      ]
    }
  }
]
```

Get info on all of the plugins that are currently registered with Synse Server.

This endpoint makes it easy to see which plugins are registered with an instance of Sysne Server.
It exposes metadata about the plugin, plugin config info, and the health status of that plugin.

### HTTP Request

`GET http://host:5000/synse/v2/plugins`

### Response

| Field | Description |
| ----- | ----------- |
| *tag* | The plugin tag. This is a normalized string made up of its name and maintainer. |
| *name* | The name of plugin. |
| *maintainer* | The maintainer of the plugin. |
| *description* | A short description of the plugin. |
| *vcs* | A link to the version control repo for the plugin. |
| *version* | An object that contains version information about the plugin. |
| *{version}.plugin_version* | The plugin version. |
| *{version}.sdk_version* | The version of the Synse SDK that the plugin is using. |
| *{version}.build_date* | The date that the plugin was built. |
| *{version}.git_commit* | The git commit at which the plugin was built. |
| *{version}.git_tag* | The git tag at which the plugin was built. |
| *{version}.arch* | The architecture that the plugin is running on. |
| *{version}.os* | The OS that the plugin is running on. |
| *network* | An object that describes the network configurations for the plugin. |
| *{network}.protocol* | The protocol that is used to communicate with the plugin (unix, tcp). |
| *{network}.address* | The address of the plugin for the protocol used. |
| *health* | An object that describes the overall health of the plugin. |
| *{health}.timestamp* | The time at which the health status applies. |
| *{health}.status* | The health status of the plugin (ok, degraded, failing, error, unknown) |
| *{health}.message* | A message describing the error, if in an error state. |
| *{health}.checks* | A collection of health check snapshots for the plugin. |

There may be 0..N health checks for a Plugin, depending on how it is configured. The health
check elements here make up a snapshot of the plugin's health at a given time.

| Field | Description |
| ----- | ----------- |
| *name* | The name of the health check. |
| *status* | The status of the health check (ok, failing) |
| *message* | A message describing the failure, if in a failing state. |
| *timestamp* | The timestamp for which the status applies. |
| *type* | The type of health check (e.g. periodic) |


## Scan

```shell
curl "http://host:5000/synse/v2/scan"
```

```python
import requests

response = requests.get('http://host:5000/synse/v2/scan')
```

> The response JSON would be structured as:

```json
{
  "racks": [
    {
      "id": "rack-1",
      "boards": [
        {
          "id": "vec",
          "devices": [
            {
              "id": "0fe8f06229aa9a01ef6032d1ddaf18a5",
              "info": "Synse Temperature Sensor 3",
              "type": "temperature"
            },
            {
              "id": "12835beffd3e6c603aa4dd92127707b5",
              "info": "Synse Fan",
              "type": "fan"
            },
            {
              "id": "12ea5644d052c6bf1bca3c9864fd8a44",
              "info": "Synse LED",
              "type": "led"
            },
            {
              "id": "34c226b1afadaae5f172a4e1763fd1a6",
              "info": "Synse Humidity Sensor",
              "type": "humidity"
            },
            {
              "id": "3ee84834c79c5a124d858e237e81e186",
              "info": "Synse Temperature Sensor 2",
              "type": "temperature"
            },
            {
              "id": "45ffe8f7f7a2b0ae970b687abd06f9e6",
              "info": "Synse Temperature Sensor 1",
              "type": "temperature"
            },
            {
              "id": "8f7ac60be5c8a3815ce89753de138edf",
              "info": "Synse Temperature Sensor 5",
              "type": "temperature"
            },
            {
              "id": "bcf0618c50bff9121cb10d141d66f46f",
              "info": "Synse backup LED",
              "type": "led"
            },
            {
              "id": "df6a06d6e28da8aab0c25ee41688fd1c",
              "info": "Synse Airflow Sensor",
              "type": "airflow"
            },
            {
              "id": "e385de0e2b5d16af5e34167d479fc766",
              "info": "Synse Pressure Sensor 1",
              "type": "pressure"
            },
            {
              "id": "f441d97b2f6545ef3001a688489e820a",
              "info": "Synse Temperature Sensor 4",
              "type": "temperature"
            },
            {
              "id": "f838b2d6afceb01e7a2634893f6f935c",
              "info": "Synse Pressure Sensor 2",
              "type": "pressure"
            },
            {
              "id": "da7fbdfc8e962922685af9d0fac53379",
              "info": "Synse Door Lock",
              "type": "lock"
            }
          ]
        }
      ]
    }
  ]
}
```

Enumerate all known devices that Synse Server can access via its plugins, grouped by rack and board.

The `scan` endpoint provides an aggregated view of the devices, organized by their rack and board
locations, which are made known to Synse Server by each of the registered plugin back-ends. The
`scan` response provides a high-level view of what exists and how to route to it. This routing
information (e.g. rack ID, board ID, device ID) can be used in subsequent commands such as [read](#read),
[write](#write), and [info](#info).

By default, `scan` will enumerate all devices on all boards on all racks. The `rack` and `board` URI
parameters, defined below, can be used to refine the scan to return devices only within the scope of
the given rack or board.

The scan results are sorted by rack id, board id, and plugin.

### HTTP Request

`GET http://host:5000/synse/v2/scan[/{rack}[/{board}]]`

### URI Parameters

| Parameter | Required | Description |
| --------- | -------- | ----------- |
| *rack*    | no       | The id of the rack to scan. *Required only if specifying board.* |
| *board*   | no       | The id of the board to scan. |

### Query Parameters

| Parameter | Default | Description |
| --------- | ------- | ----------- |
| *force*   | false   | Force a re-scan of all known devices. This invalidates the existing cache, causing it to be rebuilt. *Valid values:* `true` |

### Response Fields

| Field | Description |
| ----- | ----------- |
| *racks* | A list of objects which represent a rack. |
| *{rack}.id* | The primary identifier for the rack. |
| *{rack}.boards* | A list of board object which belong to the rack. |
| *{board}.id* | The primary identifier for the board. |
| *{board}.devices* | A list of device objects which belong to the board. |
| *{device}.id* | The primary identifier for the device. |
| *{device}.info* | Any notational information associated with the device to help identify it in a more human-readable way. Note that this is not guaranteed to be unique across devices. |
| *{device}.type* | The [type](#device-types) of the device. |



## Read

```shell
curl "http://host:5000/synse/v2/read/rack-1/vec/eb100067acb0c054cf877759db376b03"
```

```python
import requests

response = requests.get('http://host:5000/synse/v2/read/rack-1/vec/eb100067acb0c054cf877759db376b03')
```

> The response JSON would be structured as:

```json
{
  "kind": "temperature",
  "data": [
    {
      "value": 20.3,
      "timestamp": "2018-02-01T13:47:40.395939895Z",
      "unit": {
        "symbol": "C",
        "name": "degrees celsius"
      },
      "type": "temperature",
      "info": ""
    }
  ]
}
```

> Devices can provide multiple readings, e.g. an LED device could give a JSON response like:

```json
{
  "kind": "led",
  "data": [
    {
      "value": "off",
      "timestamp": "2018-02-01T13:48:59.573898829Z",
      "unit": null,
      "type": "state",
      "info": ""
    },
    {
      "value": "000000",
      "timestamp": "2018-02-01T13:48:59.573898829Z",
      "unit": null,
      "type": "color",
      "info": ""
    }
  ]
}
```

Read data from a known device.

Devices may not necessarily support reading, and the reading values for one device of a given type
may not match those of a different device with the same type. That is to say, the read behavior for
a device is defined at the plugin level, and may differ from plugin to plugin or device to device.

If a read is not supported, an error will be returned with the JSON response specifying the cause
as reads not permitted.

### HTTP Request

`GET http://host:5000/synse/v2/read/{rack}/{board}/{device}`

### URI Parameters

| Parameter | Required | Description |
| --------- | -------- | ----------- |
| *rack*    | yes      | The id of the rack containing the device to read. |
| *board*   | yes      | The id of the board containing the device to read. |
| *device*  | yes      | The id of the device to read. |

These values can be found via the [scan](#scan) command.

### Response Fields

| Field | Description |
| ----- | ----------- |
| *kind*  | The kind of device that was read. See [Device Types](#device-types) for more info. |
| *data*  | An object where the keys specify the *reading type* and the values are the corresponding reading objects. Note that a reading type is not the same as the device type. |
| *{reading}.value* | The value for the given reading type. |
| *{reading}.timestamp* | The time at which the reading was taken. |
| *{reading}.type* | The type of the reading output. |
| *{reading}.info* | Any additional information associated with the reading. |
| *{reading}.unit* | The unit of measure for the reading. If the reading has no unit, this will be `null`. |
| *{unit}.name* | The long name of the unit. *(e.g. "acceleration")* |
| *{unit}.symbol* | The symbol (or short name) of the unit. *(e.g. "m/s^2")* |


## Read Cached

> The response for the `readcached` endpoint is streamed JSON. 

```shell
curl "http://host:5000/synse/v2/readcached"
```

```python
import requests
import json

response = requests.get('http://host:5000/synse/v2/readcached', stream=True)

# get each line of the streamed response as json
for chunk in response.iter_lines():
    data = json.loads(chunk) 
```

> A single line of the streamed response JSON would be structured as:

```json
{"location":{"rack":"rack-1","board":"vec","device":"34c226b1afadaae5f172a4e1763fd1a6"},"kind":"humidity","value":31,"timestamp":"2018-10-19T19:13:00.9184028Z","unit":{"symbol":"C","name":"celsius"},"type":"temperature","info":""}
```

Stream reading data from all configured plugins.

All plugins have the capability of caching their readings locally in order to maintain a higher
resolution of state beyond the poll frequency which Synse Server may request at. This is particularly
useful for push-based plugins, where we would lose the pushed reading if it were not cached. 

At the plugin level, caching read data can be enabled, but is disabled by default. Even if disabled,
this route will still return data for every device that supports reading on each of the configured
plugins. When read caching is disabled, this will just return a dump of the "current" reading state
that is maintained by the plugin.

### HTTP Request

`GET http://host:5000/synse/v2/readcached`

### Query Parameters

| Parameter | Description |
| --------- | ----------- |
| *start*   | An RFC3339 or RFC3339Nano formatted timestamp which specifies a starting bound on the cache data to return. If no timestamp is specified, there will not be a starting bound. |
| *end*     | An RFC3339 or RFC3339Nano formatted timestamp which specifies an ending bound on the cache data to return. If no timestamp is specified, there will not be an ending bound. |

### Response Fields

See the responses for [read](#read). The data here is the same, with the addition of a *kind* field, which
specifies the device kind and *location* object, which provides the routing info for the corresponding device.


## Write

```shell
curl \
  -H "Content-Type: application/json" \
  -X POST \
  -d '{"action": "color", "data": "f38ac2"}' \
  "http://host:5000/synse/v2/write/rack-1/vec/f52d29fecf05a195af13f14c7306cfed"
```

```python
import requests

data = {
    'action': 'color',
    'data': 'f38ac2'
}

response = requests.post(
    'http://host:5000/synse/v2/write/rack-1/vec/f52d29fecf05a195af13f14c7306cfed', 
    json=data
)
```

> The response JSON would be structured as:

```json
[
  {
    "context": {
      "action": "color",
      "data": "f38ac2"
    },
    "transaction": "b9keavu8n63001v6bnm0"
  }
]
```

Write data to a known device.

Devices may not necessarily support writing, and the write actions for one device of a given type
may not match those of a different device with the same type. That is to say, the write behavior for
a device is defined at the plugin level, and may differ from plugin to plugin or device to device.

If a write is not supported, an error will be returned with the JSON response specifying the cause
as writes not permitted.

The `write` endpoint does not do any data validation upfront, as it is intended to be a generalized
write command. Some "alias" routes exists which allow writing to a specific device type. For those
routes ([led](#led), [fan](#fan)), validation is done on the provided data, to the best extent it
can be.

The data POSTed for a write consists of two pieces: an `action`, and `data` field. The values for these
change based on the device type/plugin, but in general the `action` specifies what will change and
`data` is the data needed to make that change. See below for more details.

<aside class="notice">
 In Synse Server v2, the <i>data</i> field was called <i>raw</i>. For backwards compatibility,
 <i>raw</i> is still allowed, but will be phased out in the future.
</aside>


### HTTP Request

`POST http://host:5000/synse/v2/write/{rack}/{board}/{device}`

### URI Parameters

| Parameter | Required | Description |
| --------- | -------- | ----------- |
| *rack*    | yes      | The id of the rack containing the device to write to. |
| *board*   | yes      | The id of the board containing the device to write to. |
| *device*  | yes      | The id of the device to write to. |

These values can be found via the [scan](#scan) command.

### POST Body

The post body requires an "action" and "data" to be specified, e.g.

> Example POSTed JSON

```json
{
  "action": "color",
  "data": "ff0000"
}
```

| Field | Description |
| ----- | ----------- |
| *action* | The write action to perform. This is device-specific. |
| *data* | The data associated with the given action. |

The valid values and requirements for `action` and `data` are dependent on the device type/plugin
implementation. For example, an `LED` device supports the actions: `color`, `state`; a
`fan` device supports `speed`. 

Some devices may only need an `action` specified. Some may need both `action` and `data` specified.
While it is up to the underlying plugin to determine what are valid values for a device, generally,
the `action` should be the attribute to set and `data` should be the value to set it to.

### Response Fields

| Field | Description |
| ----- | ----------- |
| *context* | The write payload that was POSTed. This is included to help make transactions more identifiable. |
| *transaction* | The ID of the write transaction. Each write will have its own ID. The status of a transaction can be checked with the [transaction](#transaction) command. |



## Transaction

```shell
curl "http://host:5000/synse/v2/transaction/b9pin8ofmg5g01vmt77g"
```

```python
import requests

response = requests.get('http://host:5000/synse/v2/transaction/b9pin8ofmg5g01vmt77g')
```

> The response JSON would be structured as:

```json
{
  "id": "b9pin8ofmg5g01vmt77g",
  "context": {
    "action": "color",
    "data": "f38ac2"
  },
  "state": "ok",
  "status": "done",
  "created": "2018-02-01T15:00:51.132823149Z",
  "updated": "2018-02-01T15:00:51.132823149Z",
  "message": ""
}
```

> To list all cached transactions:

```shell
curl "http://host:5000/synse/v2/transaction"
```

```python
import requests

response = requests.get('http://host:5000/synse/v2/transaction')
```

> The response JSON would be structured as:

```json
[
  "b9pin8ofmg5g01vmt77g",
  "baqgsm0if78g01rr9vqg"
]
```


Check the state and status of a write transaction.

If no transaction ID is given, a list of all cached transaction IDs is returned. The length
of time that a transaction is cached for is configurable. See the Synse Server configuration
[Configuration Documentation](http://synse-server.readthedocs.io/en/latest/user/configuration.html)
for more.

### HTTP Request

`GET http://host:5000/synse/v2/transaction[/{transaction id}]`

### URI Parameters

| Parameter | Required | Description |
| --------- | -------- | ----------- |
| *transaction id* | no | The ID of the write transaction to get the status of. This is given by the corresponding [write](#write). |

### Response Fields

| Field | Description |
| ----- | ----------- |
| *id*      | The ID of the transaction. |
| *context* | The POSTed write data for the given write transaction. |
| *state*   | The current state of the transaction. *Valid values:* (`ok`, `error`) |
| *status*  | The current status of the transaction. *Valid values:* (`unknown`, `pending`, `writing`, `done`)|
| *created* | The time at which the transaction was created (e.g. the write issued). |
| *updated* | The last time the state or status was updated for the transaction. If the transaction has state `ok` and status `done`, no further updates will occur. |
| *message* | Any context information for the transaction relating to its error state. If there is no error, this will be an empty string. |


## Info

> The `info` endpoint will return different responses based on the scope of the request. For 
> a rack-level request:

```shell
curl "http://host:5000/synse/v2/info/rack-1"
```

```python
import requests

response = requests.get('http://host:5000/synse/v2/info/rack-1')
```

> The response JSON would be structured as:

```json
{
  "rack": "rack-1",
  "boards": [
    "vec"
  ]
}
```

> For a board-level request:

```shell
curl "http://host:5000/synse/v2/info/rack-1/vec"
```

```python
import requests

response = requests.get('http://host:5000/synse/v2/info/rack-1/vec')
```

> The response JSON would be structured as:

```json
{
  "board": "vec",
  "location": {
    "rack": "rack-1"
  },
  "devices": [
    "eb9a56f95b5bd6d9b51996ccd0f2329c",
    "f52d29fecf05a195af13f14c7306cfed",
    "d29e0bd113a484dc48fd55bd3abad6bb",
    "eb100067acb0c054cf877759db376b03",
    "83cc1efe7e596e4ab6769e0c6e3edf88",
    "db1e5deb43d9d0af6d80885e74362913",
    "329a91c6781ce92370a3c38ba9bf35b2",
    "f97f284037b04badb6bb7aacd9654a4e"
  ]
}
```

> For a device-level request:

```shell
curl "http://host:5000/synse/v2/info/rack-1/vec/db1e5deb43d9d0af6d80885e74362913"
```

```python
import requests

response = requests.get('http://host:5000/synse/v2/info/rack-1/vec/db1e5deb43d9d0af6d80885e74362913')
```

> The response JSON would be structured as:

```json
{
  "timestamp": "2018-06-18T13:30:15.6554449Z",
  "uid": "34c226b1afadaae5f172a4e1763fd1a6",
  "kind": "humidity",
  "metadata": {
    "model": "emul8-humidity"
  },
  "plugin": "emulator plugin",
  "info": "Synse Humidity Sensor",
  "location": {
    "rack": "rack-1",
    "board": "vec"
  },
  "output": [
    {
      "name": "humidity",
      "type": "humidity",
      "precision": 3,
      "scaling_factor": 1.0,
      "unit": {
        "name": "percent humidity",
        "symbol": "%"
      }
    },
    {
      "name": "temperature",
      "type": "temperature",
      "precision": 3,
      "scaling_factor": 1.0,
      "unit": {
        "name": "celsius",
        "symbol": "C"
      }
    }
  ]
}
```

Get the available information for the specified resource.

### HTTP Request

`GET http://host:5000/synse/v2/info/{rack}[/{board}[/{device}]]`

### URI Parameters

| Parameter | Required | Description |
| --------- | -------- | ----------- |
| *rack*    | yes      | The id of the rack to get info for. |
| *board*   | no       | The id of the board to get info for. *Required only if specifying device.* |
| *device*  | no       | The id of the device to get info for. |

### Response Fields

***Rack Level Response***

| Field | Description |
| ----- | ----------- |
| *rack* | The ID of the rack. |
| *boards* | A list of IDs for boards that belong to the rack. |

***Board Level Response***

| Field | Description |
| ----- | ----------- |
| *board* | The ID of the board. |
| *location* | An object which provides information on its hierarchical parents (e.g. rack). |
| *devices* | A list of IDs for devices that belong to the board. |

***Device Level Response***

| Field | Description |
| ----- | ----------- |
| *timestamp* | The time at which the device info was last retrieved. |
| *uid* | The unique (per board) ID of the device. |
| *kind* | The device kind, as specified by the plugin. The last element in the namespaced name should be the device type. |
| *metadata* | A mapping of arbitrary values that provide metadata for the device. |
| *plugin* | The name of the plugin that manages the device. |
| *info* | Any human-readable information set to help identify the given device. |
| *location* | An object which provides information on its hierarchical parents (e.g. rack, board). |
| *output* | A list of output types that this device supports. |



## LED

> If no *valid* query parameters are specified, this will **read** from the LED device.

```shell
curl "http://host:5000/synse/v2/led/rack-1/vec/f52d29fecf05a195af13f14c7306cfed"
```

```python
import requests

response = requests.get('http://host:5000/synse/v2/led/rack-1/vec/f52d29fecf05a195af13f14c7306cfed')
```

> The response JSON will be the same as read response:

```json
{
  "kind": "led",
  "data": [
    {
      "value": "off",
      "timestamp": "2018-02-01T16:16:04.884816422Z",
      "unit": null,
      "type": "state",
      "info": ""
    },
    {
      "value": "f38ac2",
      "timestamp": "2018-02-01T16:16:04.884816422Z",
      "unit": null,
      "type": "color",
      "info": ""
    }
  ]
}
```

> If any *valid* query parameters are specified, this will **write** to the LED device.

```shell
curl "http://host:5000/synse/v2/led/rack-1/vec/f52d29fecf05a195af13f14c7306cfed?color=00ff00&state=on"
```

```python
import requests

response = requests.get('http://host:5000/synse/v2/led/rack-1/vec/f52d29fecf05a195af13f14c7306cfed?color=00ff00&state=on')
```

> The response JSON will be the same as a write response:

```json
[
  {
    "context": {
      "action": "state",
      "data": "on"
    },
    "transaction": "b9pjujgfmg5g01vmt7b0"
  },
  {
    "context": {
      "action": "color",
      "data": "00ff00"
    },
    "transaction": "b9pjujgfmg5g01vmt7bg"
  }
]
```


An alias to `read` from or `write` to a known LED device.

While an LED device can be read directly via the [read](#read) route or written to directly from the
[write](#write) route, this route provides some additional checks and validation before dispatching to
the appropriate plugin handler. In particular, it checks if the specified device is an LED device and
that the given query parameter value(s), if any, are permissible.

If no valid query parameters are specified, this endpoint will read the specified device. If any number
of valid query parameters are specified, the endpoint will write to the specified device.

Invalid query parameters will result in a 400 Invalid Arguments error.

### HTTP Request

`GET http://host:5000/synse/v2/led/{rack}/{board}/{device}`

### URI Parameters

| Parameter | Required | Description |
| --------- | -------- | ----------- |
| *rack*    | yes      | The id of the rack containing the LED device to read from/write to. |
| *board*   | yes      | The id of the board containing the LED device to read from/write to. |
| *device*  | yes      | The id of the LED device to read from/write to. |

### Query Parameters

| Parameter | Description |
| --------- | ----------- |
| *state*   | The state of the LED. *Valid values:* (`on`, `off`, `blink`) |
| *color*   | The color of the LED. This must be an RGB hexadecimal color string. |

<aside class="notice">
 While Synse Server supports the listed Query Parameters, not all devices will support the 
 corresponding actions. As a result, writing to some <i>LED</i> instances may result in error.
</aside>

### Response Fields

See the responses for [read](#read) and [write](#write).


## Fan

> If no *valid* query parameters are specified, this will **read** from the fan device.

```shell
curl "http://host:5000/synse/v2/fan/rack-1/vec/eb9a56f95b5bd6d9b51996ccd0f2329c"
```

```python
import requests

response = requests.get('http://host:5000/synse/v2/fan/rack-1/vec/eb9a56f95b5bd6d9b51996ccd0f2329c')
```

> The response JSON will be the same as read response:

```json
{
  "kind": "fan",
  "data": [
    {
      "value": 0,
      "timestamp": "2018-02-01T17:07:18.113960446Z",
      "unit": {
        "symbol": "RPM",
        "name": "revolutions per minute"
      },
      "type": "fan_speed",
      "info": ""
    }
  ]
}
```

> If any *valid* query parameters are specified, this will **write** to the fan device.

```shell
curl "http://host:5000/synse/v2/fan/rack-1/vec/eb9a56f95b5bd6d9b51996ccd0f2329c?speed=200"
```

```python
import requests

response = requests.get('http://host:5000/synse/v2/fan/rack-1/vec/eb9a56f95b5bd6d9b51996ccd0f2329c?speed=200')
```

> The response JSON will be the same as a write response:

```json
[
  {
    "context": {
      "action": "speed",
      "data": "200"
    },
    "transaction": "b9pkjh8fmg5g01vmt7d0"
  }
]
```

An alias to `read` from or `write` to a known fan device.

While a fan device can be read directly via the [read](#read) route or written to directly from the
[write](#write) route, this route provides some additional checks and validation before dispatching to
the appropriate plugin handler. In particular, it checks if the specified device is a fan device and
that the given query parameter value(s), if any, are permissible.

If no valid query parameters are specified, this endpoint will read the specified device. If any number
of valid query parameters are specified, the endpoint will write to the specified device.

Invalid query parameters will result in a 400 Invalid Arguments error.

### HTTP Request

`GET http://host:5000/synse/v2/fan/{rack}/{board}/{device}`

### URI Parameters

| Parameter | Required | Description |
| --------- | -------- | ----------- |
| *rack*    | yes      | The id of the rack containing the fan device to read from/write to. |
| *board*   | yes      | The id of the board containing the fan device to read from/write to. |
| *device*  | yes      | The id of the fan device to read from/write to. |

### Query Parameters

| Parameter | Description |
| --------- | ----------- |
| *speed* | The speed (in RPM) to set the fan to. |
| *speed_percent* | The speed (in percent) to set the fan to. |

<aside class="notice">
 While Synse Server supports the listed Query Parameters, not all devices will support the 
 corresponding actions. As a result, writing to some <i>fan</i> instances may result in error.
</aside>

### Response Fields

See the responses for [read](#read) and [write](#write).


## Power

> If no *valid* query parameters are specified, this will **read** from the power device.

```shell
curl "http://host:5000/synse/v2/power/rack-1/vec/fd8e4bd57f041c1131ef965496688001"
```

```python
import requests

response = requests.get('http://host:5000/synse/v2/power/rack-1/vec/fd8e4bd57f041c1131ef965496688001')
```

> The response JSON will be the same as read response:

```json
{
  "kind": "power",
  "data": [
    {
      "value": "on",
      "timestamp": "2018-05-07T13:41:08.690629Z",
      "unit": null,
      "type": "state",
      "info": ""
    }
  ]
}
```

> If any *valid* query parameters are specified, this will **write** to the power device.

```shell
curl "http://host:5000/synse/v2/power/rack-1/vec/fd8e4bd57f041c1131ef965496688001?state=off"
```

```python
import requests

response = requests.get('http://host:5000/synse/v2/power/rack-1/vec/fd8e4bd57f041c1131ef965496688001?state=off')
```

> The response JSON will be the same as a write response:

```json
[
  {
    "context": {
      "action": "state",
      "data": "off"
    },
    "transaction": "bbo5fdtopi1g00ei06fg"
  }
]
```

An alias to `read` from or `write` to a known power device.

While a power device can be read directly via the [read](#read) route or written to directly from the
[write](#write) route, this route provides some additional checks and validation before dispatching to
the appropriate plugin handler. In particular, it checks if the specified device is a power device and
that the given query parameter value(s), if any, are permissible.

If no valid query parameters are specified, this endpoint will read the specified device. If any number
of valid query parameters are specified, the endpoint will write to the specified device.

Invalid query parameters will result in a 400 Invalid Arguments error.

### HTTP Request

`GET http://host:5000/synse/v2/power/{rack}/{board}/{device}`

### URI Parameters

| Parameter | Required | Description |
| --------- | -------- | ----------- |
| *rack*    | yes      | The id of the rack containing the power device to read from/write to. |
| *board*   | yes      | The id of the board containing the power device to read from/write to. |
| *device*  | yes      | The id of the power device to read from/write to. |

### Query Parameters

| Parameter | Description |
| --------- | ----------- |
| *state* | The power state, e.g. `on`, `off` |

<aside class="notice">
 While Synse Server supports the listed Query Parameters, not all devices may support the 
 corresponding actions. As a result, writing to some <i>power</i> instances may result in error.
</aside>

The power `state`, commonly `on`/`off`, is not bound to those values. It is up to the underlying
plugin what power actions are available. For example, the IPMI plugin supports `on`, `off`, `reset`,
and `cycle`.


### Response Fields

See the responses for [read](#read) and [write](#write).


## Boot Target

> If no *valid* query parameters are specified, this will **read** from the boot target device.

```shell
curl "http://host:5000/synse/v2/boot_target/rack-1/vec/558828ddb1b4e2a9b2e14a28a1eebd18"
```

```python
import requests

response = requests.get('http://host:5000/synse/v2/boot_target/rack-1/vec/558828ddb1b4e2a9b2e14a28a1eebd18')
```

> The response JSON will be the same as read response:

```json
{
  "kind": "boot_target",
  "data": [
    {
      "value": "disk",
      "timestamp": "2018-05-07T13:59:53.5529982Z",
      "unit": null,
      "type": "target",
      "info": ""
    }
  ]
}
```

> If any *valid* query parameters are specified, this will **write** to the boot_target device.

```shell
curl "http://host:5000/synse/v2/boot_target/rack-1/vec/558828ddb1b4e2a9b2e14a28a1eebd18?target=pxe"
```

```python
import requests

response = requests.get('http://host:5000/synse/v2/boot_target/rack-1/vec/558828ddb1b4e2a9b2e14a28a1eebd18?target=pxe')
```

> The response JSON will be the same as a write response:

```json
[
  {
    "context": {
      "action": "target",
      "data": "pxe"
    },
    "transaction": "bbo5o0a8qtig00eqhue0"
  }
]
```

An alias to `read` from or `write` to a known boot_target device.

While a boot_target device can be read directly via the [read](#read) route or written to directly from the
[write](#write) route, this route provides some additional checks and validation before dispatching to
the appropriate plugin handler. In particular, it checks if the specified device is a boot_target device and
that the given query parameter value(s), if any, are permissible.

If no valid query parameters are specified, this endpoint will read the specified device. If any number
of valid query parameters are specified, the endpoint will write to the specified device.

Invalid query parameters will result in a 400 Invalid Arguments error.

### HTTP Request

`GET http://host:5000/synse/v2/boot_target/{rack}/{board}/{device}`

### URI Parameters

| Parameter | Required | Description |
| --------- | -------- | ----------- |
| *rack*    | yes      | The id of the rack containing the boot_target device to read from/write to. |
| *board*   | yes      | The id of the board containing the boot_target device to read from/write to. |
| *device*  | yes      | The id of the boot_target device to read from/write to. |

### Query Parameters

| Parameter | Description |
| --------- | ----------- |
| *target* | The boot target to set. The values for this depend on plugin. Some examples include: `disk`, `pxe`, `none` |

<aside class="notice">
 While Synse Server supports the listed Query Parameters, not all devices will support the 
 corresponding actions. As a result, writing to some <i>boot_target</i> instances may result in error.
</aside>

### Response Fields

See the responses for [read](#read) and [write](#write).


## Lock

> If no *valid* query parameters are specified, this will **read** from the lock device.

```shell
curl "http://host:5000/synse/v2/lock/rack-1/vec/da7fbdfc8e962922685af9d0fac53379"
```

```python
import requests

response = requests.get('http://host:5000/synse/v2/lock/rack-1/vec/da7fbdfc8e962922685af9d0fac53379')
```

> The response JSON will be the same as read response:

```json
{
  "kind": "lock",
  "data": [
    {
      "value": "locked",
      "timestamp": "2018-11-27T13:47:19.998713947Z",
      "unit": null,
      "type": "state",
      "info": ""
    }
  ]
}
```

> If any *valid* query parameters are specified, this will **write** to the lock device.

```shell
curl "http://host:5000/synse/v2/lock/rack-1/vec/da7fbdfc8e962922685af9d0fac53379?action=unlock"
```

```python
import requests

response = requests.get('http://host:5000/synse/v2/lock/rack-1/vec/da7fbdfc8e962922685af9d0fac53379?action=unlock')
```

> The response JSON will be the same as a write response:

```json
[
  {
    "context": {
      "action": "unlock"
    },
    "transaction": "gbo5t0a8atig19jnhue1"
  }
]
```

An alias to `read` from or `write` to a known lock device.

While a lock device can be read directly via the [read](#read) route or written to directly from the
[write](#write) route, this route provides some additional checks and validation before dispatching to
the appropriate plugin handler. In particular, it checks if the specified device is a lock device and
that the given query parameter value(s), if any, are permissible.

If no valid query parameters are specified, this endpoint will read the specified device. If any number
of valid query parameters are specified, the endpoint will write to the specified device.

Invalid query parameters will result in a 400 Invalid Arguments error.

### HTTP Request

`GET http://host:5000/synse/v2/lock/{rack}/{board}/{device}`

### URI Parameters

| Parameter | Required | Description |
| --------- | -------- | ----------- |
| *rack*    | yes      | The id of the rack containing the lock device to read from/write to. |
| *board*   | yes      | The id of the board containing the lock device to read from/write to. |
| *device*  | yes      | The id of the lock device to read from/write to. |

### Query Parameters

| Parameter | Description |
| --------- | ----------- |
| *action* | The state to set the fan to. *Valid values:* (`lock`, `unlock`, `pulseUnlock`) |

<aside class="notice">
 While Synse Server supports the listed Query Parameters, not all devices will support the 
 corresponding actions. As a result, writing to some <i>lock</i> instances may result in error.
</aside>

### Response Fields

See the responses for [read](#read) and [write](#write).

