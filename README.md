# Installation

```
git clone https://github.com/sidahmed-malaoui/action_after_operation

sudo mv act/act.py /usr/local/bin/act
```

# Usage
```act -o operation_to_wait_for -a action_to_perform -v```

# Examples 
Shutdown the pc after the end of a copy :
```act -o copy -a poweroff -v```

Reboot the pc after the end of a download :
```act -o download -a reboot -v```

The -v option stands for verbose. You better use it to see what is happening while you are waiting for the end of the operation.
