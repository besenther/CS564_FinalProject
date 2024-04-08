import subprocess

# Define the command to execute
command = ["ls"]  # Example command
process = subprocess.Popen(command, stdout=subprocess.PIPE)
output = []

for i in process.stdout.readlines():
    output.append(i.decode().strip())

print(output)