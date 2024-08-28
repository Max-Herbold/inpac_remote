# NOT USED ANYWHERE


import os

import dotenv

# Load the environment variables
dotenv.load_dotenv()

token = os.getenv("GITHUB_TOKEN")

# run git pull
command = (
    f"git pull https://Max-Herbold:{token}@github.com/Max-Herbold/inpac_remote.git"
)
print("running pull", command)

# git pull https://Max-Herbold:***@github.com/Max-Herbold/inpac_remote.git
os.system(command)
