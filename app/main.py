from database import Database
from login_screen import login_screen

# docker build -t urban_mobility_system .
# docker run -it --rm -v ${PWD}/data:/app/data urban_mobility_system WUKI
# docker run -it --rm -v $(pwd)/data:/app/data urban_mobility_system

if __name__ == "__main__":
    database = Database("data/database.db")
    login_screen()
