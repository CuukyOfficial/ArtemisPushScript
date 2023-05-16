import os

types = {
    "Exercise": "exercise",
    "Solution": "solution",
    "Tests": "tests"
}

print("ArtemisTransferScript v0.1 by Cuuky")
print("NOTE: The script will only work if you have a valid Artemis task directory. "
      "The directory should contain the following folders:")

for key in types:
    print(key)

print("The script also will delete any files in the cloned repository and replace them with the given files.")

directory = ""
# Get task name
while True:
    directory = input("Enter directory of tasks: ")
    if directory != "":
        break
    print("Please enter a valid directory")

working_dir = ""
# Get working directory
while True:
    working_dir = input("Enter directory where the repositories should be cloned into: ")
    if working_dir != "":
        break
    print("Please enter a valid directory")

extra_git_commands = []
# Check if user wants extra git inputs
while True:
    print("Now enter extra git commands that will be executed in every cloned directory (leave empty if finished): ")
    command = input()
    if command == "":
        break
    extra_git_commands.append(command)

for key in types:
    git_url = input("Enter git url for " + key + ": ")

    # Check if directory exists
    if not os.path.isdir(directory + "/" + key):
        print("Directory " + directory + "/" + key + " does not exist, skipping...")
        continue

    # Check if git repository exists
    if os.path.isdir(working_dir + "/" + key):
        print("Directory " + working_dir + "/" + types[key] + " already exists, skipping...")
        continue

    # Clone git repository
    os.system("git clone " + git_url + " " + working_dir + "/" + types[key])

    working_dir_temp = working_dir + "/" + types[key]

    # Execute extra git commands
    for command in extra_git_commands:
        os.system("cd " + working_dir_temp + " && " + command)

    # Delete files in repository
    os.system("rm -rf " + working_dir + "/" + types[key] + "/*")

    # Copy files from task directory to repository
    os.system("cp -r " + directory + "/" + key + "/* " + working_dir_temp)

    # Add files to git
    os.system("cd " + working_dir_temp + "/" + types[key] + " && git add .")

    # Commit files
    os.system("cd " + working_dir_temp + "/" + types[key] + " && git commit -m \"Initial commit\"")

    # Push files
    os.system("cd " + working_dir_temp + "/" + types[key] + " && git push")

    print("Successfully cloned " + key + " repository")

print("Successfully cloned all repositories")
