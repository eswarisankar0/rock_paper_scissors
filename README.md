Mystic Duel — Rock Paper Scissors

A mystical Rock Paper Scissors web game built with **Python Flask**, containerized with **Docker**, and deployed through a **Jenkins CI/CD pipeline**.

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.x-black?style=flat-square&logo=flask)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=flat-square&logo=docker)
![Jenkins](https://img.shields.io/badge/Jenkins-CI%2FCD-D24939?style=flat-square&logo=jenkins)

---

## About the App

A browser-based Rock Paper Scissors game with a beautiful **space/mystic theme**. The player challenges the computer, which picks a random move each round. The app tracks your **Wins**, **Draws**, and **Losses** across the session.

**Features:**
- Animated starry/cosmic background
- Glowing interactive buttons for Rock , Paper , and Scissors 
- Live scoreboard showing Wins / Draws / Losses
- Fully responsive — works on desktop and mobile
- Runs entirely in the browser via Flask's template rendering

---

##  Project Structure

```
rock_paper_scissors/
├── app.py               # Flask app with game logic and HTML template
├── requirements.txt     # Python dependency (Flask)
├── Dockerfile           # Docker image build instructions
├── Jenkinsfile          # Jenkins CI/CD pipeline (5 stages)
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

---

##  Running Locally (without Docker)

```bash
# 1. Clone the repository
git clone https://github.com/eswarisankar0/rock_paper_scissors.git
cd rock_paper_scissors

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python app.py
```

Open your browser at: **http://localhost:5000**

---

##  Running with Docker

### Pull from DockerHub and run:

```bash
docker pull <dockerhub_uname>/rock-paper-scissors:latest

docker run -d -p 5000:5000 --name rps-app <dockerhub_uname>/rock-paper-scissors:latest
```

Open your browser at: **http://localhost:5000**

### Build and run locally:

```bash
# Build the image
docker build -t stone-paper-scissors .

# Run the container
docker run -d -p 5000:5000 --name rps-app stone-paper-scissors
```

### Stop the container:

```bash
docker stop rps-app
docker rm rps-app
```

---

##  Jenkins CI/CD Pipeline

The `Jenkinsfile` defines a **5-stage pipeline** that fully automates build, test, and deployment:

| Stage | Description |
|-------|-------------|
| **1. Clone** | Checks out the source code from GitHub |
| **2. Build** | Installs Python dependencies from `requirements.txt` |
| **3. Docker Build** | Builds the Docker image tagged with the Jenkins build number |
| **4. Push to DockerHub** | Pushes both `:latest` and `:<build_number>` tags to DockerHub |
| **5. Deploy** | Stops any existing container and runs the new image on port 5000 |

### Jenkins Setup Instructions

1. Install **Jenkins** with the **Docker Pipeline** plugin
2. Add DockerHub credentials in Jenkins:
   - Go to Manage Jenkins → Credentials
   - Add a Username/Password credential
   - Set the ID to: `devops-dockerhub`
3. Create a new Pipeline job and point it to this repository
4. Push any change to `main` — the pipeline triggers automatically

---

## Required Jenkins Credentials

| Credential ID | Type | Description |
|---------------|------|-------------|
| `devops-dockerhub` | Username / Password | DockerHub login to push the Docker image |


## Git Workflow

- All changes are pushed to feature branches and merged via **Pull Requests** only
- Direct pushes to `main` are discouraged
- Each commit carries a meaningful message describing the change made
- `.gitignore` prevents `__pycache__`, `.env`, and other unnecessary files from being tracked


## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.11 | Core programming language |
| Flask | Web framework & HTML templating |
| Docker | Containerization |
| DockerHub | Container image registry |
| Jenkins | CI/CD pipeline automation |
| GitHub | Version control & code collaboration |
