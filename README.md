ASSET STORE CODING CHALLENGE
============================

This is a solution to the problem posed [here](https://gist.github.com/bcavagnolo/14a869f0e9df6f37d203cc832ec1125d)
by Planet Labs.



### Supported Functionality and Use
As required by the specification, this REST API allows the user to:
- Create an asset
- Retrieve a single asset by name
- Retrieve a list of assets

Additionally, it supports:
- Providing key/value pair details associated to a particular asset, with validation for appropriate detail keys based on the asset type/class
- API URLs supporting filtering by asset type or class
- In order to create an asset, the `X-User: admin` header must be used
- An admin auto-generated GUI to view the data

The API is hosted on heroku! Please feel free to test it out. The URL is:

[asset-store.herokuapp.com](http://asset-store.herokuapp.com)

To access the admin site, go to the following link and ask me for a login:

[asset-store.herokuapp.com/admin](http://asset-store.herokuapp.com/admin)

All of the following API resources are prefixed by `http://asset-store.herokuapp.com/apiv1`:

| METHOD | URL | DESCRIPTION |
|--------|-----|-------------|
| GET | `/assets/` | Get a list of all assets |
| POST | `/assets/` | Create a new asset |
| GET | `/assets/<class>/classfilter/` | Get a list of assets, filtered by the given class |
| GET | `/assets/<type>/typefilter/` | Get a list of assets, filtered by the given type |
| GET | `/assets/<name>/` | Fetch the particular asset with the given name |

For all of the list types, you should expect a JSON list including the information of all of the assets, including its details. Getting a particular asset simply returns the JSON for that asset.

In order to create an asset, you need to provide a JSON body containing the necessary information. Here are some examples:

```
{
  "name": "sat1",
  "asset_type": "satellite",
  "asset_class": "rapideye",
  "details": []
}
```

```
{
  "name": "cool_antenna",
  "asset_type": "antenna",
  "asset_class": "dish",
  "details": [
    {
      "key": "radome",
      "val_type": "B",
      "val": "1"
    },
    {
      "key": "diameter",
      "val_type": "F",
      "val": "20"
    }
  ]
}
```
The `val_type` supports the following:
- B for boolean
- F for float
- I for integer
- S for string (can be unicode as well)


### Implementation Details
My implementation leverages two very powerful open source packages, Django and Django REST Framework. Django allowed me to define the models in a concise manner, which then abstracts away all SQL queries as python objects and function calls. This allowed me to quickly add all of the extra functionality and more complex relationships between objects. Django REST Framework allowed me to leverage their auto generated serializers based on the Django models. Finally, I used Heroku to host my app and try it out over the Internet, as well as making it available to anyone interested in testing it. It is running with Postgresql as the database backend.

### Building and Running
If you would like to run the code on your own computer, simply download or clone this repo, crate a python virtual environment, and run the following to launch the application on your localhost:

```
pip install -r requirements.txt
python manage.py collectstatic
python manage.py runserver
```
