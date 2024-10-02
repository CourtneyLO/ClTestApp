# IOS

## Running App on Real Device

### Local Backend

Set your ip address in replace of your IP address on the frontend i.e:

Change:
```
const httpLink = createHttpLink({
  uri: 'http://127.0.0.1:8000/graphql',,
});
```

To this:
```
const httpLink = createHttpLink({
  uri: 'http://192.168.xx.xx:8000/graphql',
});
```

Add IP to ALLOWED_HOSTS in .env

Run the following

```
$ python manage.py runserver 0.0.0.0:8000
```

#### Find IP address

On Mac:

Apple Icon -> System Settings -> Wi-Fi -> Details -> Ip Address
