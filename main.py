# lobman is the unofficial package manager for the LOB (Line of Business) framework. It is used to manage dependencies, install packages, and handle updates for Lobster programming languge
import os
import subprocess
import sys
import requests
if __name__ == "__main__":
    # Check if the user has provided a command
    if len(sys.argv) < 2:
        print("Usage: lobman <command> [options]")
        sys.exit(1)

    command = sys.argv[1]
    match command:
        case "install":
            url = sys.argv[2] if len(sys.argv) > 2 else None
            if not url:
                print("Please specify a URL for the package to install.")
                sys.exit(1)
            else:
                # fetch the package from the github repository and install it packages must have a pachage.lml file
                print(f"Installing package from url: {url}")
                response = requests.get(f"{url}/package.lml")
                if response.status_code == 200:
                    package_info = response.text
                    # check if the package.lml file contains the required fields
                    package_name = sys.argv[3] if len(sys.argv) > 3 else None
                    if "name" in package_info and "version" in package_info:
                        # create a directory for the package
                        os.makedirs(f"packages/{package_name}", exist_ok=True)
                        # write the package.lml file to the package directory
                        with open(f"packages/{package_name}/package.lml", "w") as f:
                            f.write(package_info)
                        print(f"Package {package_name} installed successfully.")
                    else:
                        print(f"Package {package_name} is missing required fields in package.lml.")
                        sys.exit(1)

    # Handle different commands
    if command == "install":
        url = sys.argv[2] if len(sys.argv) > 2 else None
        if not url:
            print("Please specify a URL for the package to install.")
            sys.exit(1)
        # Simulate package installation
        print(f"Installing package from url: {url}")
        subprocess.run(["git", "clone", url, f"packages/{sys.argv[3]}"])
        with open("dependencies.txt", "a") as f:
            if sys.argv[3] not in open("dependencies.txt").read():
                f.write(f"{sys.argv[3]}\n")
        packages = []
        with open("dependencies.txt", "r") as f:
            packages = [line.strip() for line in f.readlines()]
        # Here you would add the logic to install the package
        with open(".test.bat", "w") as f:
            f.write(f"@echo off\n")
            import_args = " ".join(f"--import packages/{p}" for p in packages)
            f.write(f"lobster main.lobster --import src {import_args}\n")
    elif command == "new":
        subcommand = sys.argv[2] if len(sys.argv) > 2 else None
        match subcommand:
            case "package":
                package_name = sys.argv[3] if len(sys.argv) > 3 else None
                if not package_name:
                    print("Please specify a name for the new package.")
                    sys.exit(1)
                else:
                    # create a new package directory with a package.lml file
                    os.makedirs(f"packages/{package_name}", exist_ok=True)
                    with open(f"packages/{package_name}/package.lml", "w") as f:
                        f.write(f"name: {package_name}\nversion: 0.1.0\ndescription: A new Lobster package\n")
                    print(f"New package {package_name} created successfully.")
            case "project":
                project_name = sys.argv[3] if len(sys.argv) > 3 else None
                if not project_name:
                    print("Please specify a name for the new project.")
                    sys.exit(1)
                else:
                    # create a new project directory with a main.lobster file
                    os.makedirs(f"{project_name}/src", exist_ok=True)
                    with open(f"{project_name}/src/main.lobster", "w") as f:
                        f.write(f"// {project_name} main file\n")
                    with open(f"{project_name}/dependencies.txt", "w") as f:
                        f.write("")
                    with open(f"{project_name}/.test.bat", "w") as f:
                        f.write(f"@echo off\n")
                        f.write(f"lobster src/main.lobster --import src\n")
                    print(f"New project {project_name} created successfully.")
            case "mod":
                module_name = sys.argv[3] if len(sys.argv) > 3 else None
                if not module_name:
                    print("Please specify a name for the new module.")
                    sys.exit(1)
                else:
                    if os.path.exists("src"):
                        with open(f"src/{module_name}.lobster", "w") as f:
                            f.write(f"namespace {module_name}\n")
                            f.write(f"// {module_name} module file\n")
                    else:
                        with open(f"{module_name}.lobster", "w") as f:
                            f.write(f"namespace {module_name}\n")
                            f.write(f"// {module_name} module file\n")

            case _:
                print(f"Unknown subcommand for 'new': {subcommand}")
                sys.exit(1)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
