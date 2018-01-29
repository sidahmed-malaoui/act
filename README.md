# Note
This program is not maintained for now, and it contains some bugs.

# Installation
For Debian based distros (like Ubuntu), you can download the .deb package from here https://github.com/sidahmed-malaoui/act/releases, and install it with :

```dpkg -i act_i386_amd64.deb```

# Usage
```act -o operation_to_wait_for -a action_to_perform -v```

# Examples 
Shutdown the pc after the end of a copy :
```act -o copy -a poweroff -v```

Reboot the pc after the end of a download :
```act -o download -a reboot -v```

The -v option stands for verbose. You better use it to see what is happening while you are waiting for the end of the operation.
