from database import Database
# docker build -t urban_mobility_system .
# docker run -it --rm -v $(pwd)/data:/app/data urban_mobility_system
# docker run -it --rm -v $(cd)/data:/app/data urban_mobility_system WUKI

print("Hello World!")
database = Database("data/database.db")
