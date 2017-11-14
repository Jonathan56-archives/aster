# ASTER

## QuickStart
Install Aster in your python environment
*(use pip "-e" flag for the developer mode)*:
``` ShellSession
git clone https://github.com/Jonathan56/aster.git aster
pip install .
```

To create a project open a Python console:
``` Python console
import aster
aster.new('PROJECT_PATH')
exit()
```

In order to run a simulation, you must first create a "timeline" describing events
happening during a time frame of the simulation. To do so, open "create timeline",
and run all the cells.

To launch a simulation just run:
``` ShellSession
python script.py
```

Finally, to see the results of a simulation, you need to parse the simulation log.
To do so, open "plot simulation results" and run all the cells.

## To do list:
- improve the plug and play approach
- add propellant logic
- save unused propellant
- add time constraint for launching from the same launchpad
