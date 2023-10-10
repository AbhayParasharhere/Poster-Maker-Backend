## Installation

### Prerequisites
Before you begin, ensure that you have the following prerequisites installed on your system:

1. **Docker:** You need to have Docker installed on your machine. If you haven't installed it yet, you can download it from the [official Docker website](https://www.docker.com/get-started).

### Installation Steps

1. **Clone the Repository:**
   - First, clone the Poster-Maker-Backend repository to your local machine using Git:
     ```
     git clone https://github.com/AbhayParasharhere/Poster-Maker-Backend.git
     ```

2. **Navigate to the Project Directory:**
   - Move into the project directory using the `cd` command:
     ```
     cd Poster-Maker-Backend
     ```

3. **Build Docker Images:**
   - Build the Docker images required for the project:
     ```
     docker image build -t poster-maker-backend .
     ```

4. **Build Docker Compose Services:**
   - Build the Docker Compose services defined in the `docker-compose.yml` file:
     ```
     docker-compose build
     ```

5. **Run Docker Compose:**
   - Start the Docker Compose services, which will launch your Poster Maker backend application and any associated services:
     ```
     docker-compose up
     ```

6. **Access the Application:**
   - Once the containers are up and running, you can access the Poster Maker backend by opening a web browser and navigating to `http://localhost:8000` or the appropriate URL if you have configured a different host or port.

7. **Shutdown the Application:**
   - To stop the application and shut down the Docker containers, you can use `Ctrl+C` in the terminal where you started `docker-compose up`.

That's it! You've successfully installed and launched the Poster Maker Backend using Docker. You can now start using the application as needed.
