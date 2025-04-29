# ARCA-BOT Installation and Execution Guide

This guide provides step-by-step instructions to install and run the ARCA-BOT project.

---

## Prerequisites

Ensure you have the following installed on your system:

- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose**: [Install Docker Compose](https://docs.docker.com/compose/install/)
- **Python 3.13** (if running locally without Docker): [Install Python](https://www.python.org/downloads/)

---

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd rag-arcabot
```

### 2. Set Up Environment Variables

Create a `.env` file in the root directory (if not already present) and configure the following variables:

```env
JWT_KEY='ZmFrZWp3dHNlY3JldAo='
CHATBOT_URL='http://172.17.0.1:8000'
CHROMA_PATH='/tmp/chroma_data'
```

---

## Running the Project

### Using Docker Compose

1. **Build and Start the Services**

   Run the following command to build and start the services:

   ```bash
   docker-compose up --build
   ```

2. **Access the Services**

   - **FastAPI Backend**: Accessible at [http://localhost:8000](http://localhost:8000)
   - **Streamlit Frontend**: Accessible at [http://localhost:8501](http://localhost:8501)

---

### Running Locally Without Docker

If you prefer to run the project locally without Docker, follow these steps:

#### 1. Install Dependencies

Navigate to each service directory (`arcabot_fastapi` and `arcabot_streamlit`) and install dependencies using `pip`:

```bash
cd arcabot_fastapi
pip install .

cd ../arcabot_streamlit
pip install .
```

#### 2. Start the FastAPI Backend

Navigate to the `arcabot_fastapi` directory and run the FastAPI app:

```bash
cd arcabot_fastapi/src
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

#### 3. Start the Streamlit Frontend

Navigate to the `arcabot_streamlit` directory and run the Streamlit app:

```bash
cd arcabot_streamlit/src
streamlit run main.py
```

---

## Project Structure

- **`arcabot_fastapi`**: Backend service built with FastAPI.
- **`arcabot_streamlit`**: Frontend service built with Streamlit.
- **`.env`**: Environment variables configuration.
- **`docker-compose.yml`**: Docker Compose configuration file.

---

## Troubleshooting

- **Port Conflicts**: Ensure ports `8000` and `8501` are not in use by other applications.
- **Environment Variables**: Verify that the `.env` file is correctly configured.
- **Docker Issues**: Run `docker system prune` to clean up unused Docker resources if you encounter build issues.

---

## Contact

For any issues or questions, contact **Samuele Galli** at `s.galli@arca24.com`.
```

Similar code found with 1 license type