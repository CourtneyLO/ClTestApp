# Virtual Environment

1. Create your Virtual Environment

```
$ make venv
```

2. Activate Virtual Environment

```
$ source virtualenvironment/bin/activate
```

## Other commands

### Deactivate Virtual Environment

- When you no longer need your virtual environment, this command will deactivate it.

```
$ source deactivate
```

### Remove Virtual Environment

```
$ make remove-venv
```

### Uninstall and Remove the Virtual Environment

- If something goes wrong in your virtual environment, you may need to uninstall and remove your environment.

```
$ . act-venv.sh
(virtualenvironment) $ make requirements
(virtualenvironment) $ make uninstall
(virtualenvironment) $ . deact-venv.sh
$ make remove-venv
```

- Follow the steps above to recreate your virtual environment
