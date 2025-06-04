# docker build -t urban-mobility-system .
# docker run -it --rm -v $(pwd)/data:/app/data urban-mobility-system
from login_screen import login_screen

if __name__ == "__main__":
    login_screen()
