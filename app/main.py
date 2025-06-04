from database import Database
from login_screen import login_screen
# docker build -t urban_mobility_system .
# docker run -it --rm -v $(pwd)/data:/app/data urban_mobility_system
# docker run -it --rm -v ./data:/app/data urban_mobility_system WUKI

if __name__ == "__main__":
    print("Hello World!")
    database = Database("data/database.db")
    login_screen()
