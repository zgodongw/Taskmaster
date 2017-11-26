# Taskmaster:
Leather vest, bullwhip, sadistic tendencies... LGTM.

This program is able to start jobs as child processes, and keep them alive, restart-
ing them if necessary. It also knows at all times if these processes are alive or dead.

Information on which programs must be started, how, how many, if they must be
restarted, etc... will be contained in a JSON configuration file.

## How To Run:
python3 taskmaster $1 <config path>

This program provides a controll shell that comes with the commands:
status, help, start, restart, kill, stop, reload, exit

## status:
This command shows the status of all programs descrie in the configuration file.
Usage: status

## help:
This command will print this help page.
Usage: help

## start:
This command will start a program described in the configuration file only
if it has not been started yet.
Usage: start <program>

## restart:
This command will restart a program described in the configuration file only
if it has been already started yet. (See status)
Please becareful and used the program name with the pid incase you wan to restart
a particular instance on the program else it will restart all instances of the program.
Usage: restart <program> [<pid>]

## kill:
This command will kill a program described in the configuration file with
the stopsignal described in the in the configuration file.
Please becareful and used the program name with the pid incase you want to kill
a particular instance on the program else it will kill all instances of the program.
Usage: kill <program> [<pid>]
Alternate: kill all    (this will kill all running programs)

## stop:
This command will stop a program described in the configuration file with
the stopsignal SIGKILL.
Please becareful and used the program name with the pid incase you want to stop
a particular instance on the program else it will stop all instances of the program.
Usage: stop <program> [<pid>]
Alternate: stop all    (this will stop all running programs)

## reload:
This command will reload a configuration file to the taskmaster program.
Please be very careful when using this command!
This will allow to change the attributtes of any programs you want in the
configuration file.
You can also add new programs to the configuration file if you like
but please do not remove any programs from the configuration file as this
will cause runnaway processes.
Usage: reload <configuration file name>

## exit:
This command will kill all running programs and quit the Taskmaster program.
Usage: exit
Alternate: quit
