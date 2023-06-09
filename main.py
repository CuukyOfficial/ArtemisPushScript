import os

types = {
    "Exercise": "exercise",
    "Solution": "solution",
    "Tests": "tests"
}

print("ArtemisTransferScript v0.1.1 by Cuuky")
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

for key in types:
    source_dir = os.path.join(directory, key)

    # Check if directory exists
    if not os.path.isdir(source_dir):
        print("Directory " + source_dir + " does not exist, skipping...")
        continue

    working_dir_temp = os.path.join(working_dir, types[key])

    # Check if git repository exists
    if os.path.isdir(working_dir_temp):
        print("Directory " + working_dir_temp + " already exists, skipping...")
        continue

    if not input("Do you want to push " + key + " (y/n)? ") == "y":
        continue

    git_url = input("Enter git url for " + types[key] + ": ")

    # Clone git repository
    os.system("git clone " + git_url + " " + working_dir_temp)

    # Execute extra git commands
    f = open("git.txt", "r")
    with f:
        for x in f:
            print("Executing: " + x)
            os.system("cd " + working_dir_temp + " && " + x)

    # Delete files in repository
    os.system("rm -rf " + os.path.join(working_dir_temp, "*"))

    # Copy files from task directory to repository
    os.system("cp -r " + os.path.join(source_dir, "*") + " " + working_dir_temp)

    success = input("Please enter if the directory at " + working_dir_temp + " is complete and ready to push (y/n): ")
    if success == "n" or success == "N":
        print("Skipping git add, commit and push for " + key)
        continue

    # Add files to git
    os.system("cd " + working_dir_temp + " && git add .")

    # Commit files
    os.system("cd " + working_dir_temp + " && git commit -m \"Initial commit\"")

    # Push files
    os.system("cd " + working_dir_temp + " && git push")

    print("Successfully cloned " + key + " repository")
    print("---------------\n")

print("Done.")
