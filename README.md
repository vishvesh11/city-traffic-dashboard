# Futuristic City Traffic Data Analysis Dashboard

This repository contains a dynamic and interactive Dash application designed for exploratory data analysis (EDA) of futuristic city traffic data. The dashboard provides insights into various aspects of urban mobility, including speed, traffic density, energy consumption, and their correlations with factors like economic condition, weather, and day of the week.

The application is containerized using Docker and deployed on a Kubernetes cluster, demonstrating a robust and scalable hybrid cloud deployment strategy.

## Table of Contents

  - [Features](https://www.google.com/search?q=%23features)
  - [Data Overview](https://www.google.com/search?q=%23data-overview)
  - [Technology Stack](https://www.google.com/search?q=%23technology-stack)
  - [Deployment](https://www.google.com/search?q=%23deployment)
      - [Prerequisites](https://www.google.com/search?q=%23prerequisites)
      - [Kubernetes Configuration](https://www.google.com/search?q=%23kubernetes-configuration)
      - [CI/CD Pipeline](https://www.google.com/search?q=%23ci/cd-pipeline)
  - [Usage](https://www.google.com/search?q=%23usage)
  - [Local Development](https://www.google.com/search?q=%23local-development)
  - [Contact](https://www.google.com/search?q=%23contact)

## Features

This dashboard offers comprehensive insights through the following interactive visualizations:

  - **Interactive Filters:** Filter data by `City` and `Vehicle Type` to focus on specific scenarios.
  - **Speed vs. Traffic Density Scatter Plot:** Visualize the relationship between speed and traffic density, colored by weather conditions and sized by energy consumption.
  - **Average Energy Consumption by Economic Condition:** Bar chart illustrating energy use trends across different economic states.
  - **Average Speed by Day of Week:** Bar chart showing how average speeds vary throughout the week.
  - **Average Energy Consumption by Weather:** Bar chart comparing energy consumption under different weather conditions.
  - **Correlation Matrix Heatmap:** Provides a visual representation of the correlations between all numerical features in the dataset.
  - **Dark Mode Toggle:** Switch between light and dark themes for enhanced user experience.

## Data Overview

The dashboard utilizes a synthetic dataset named `futuristic_city_traffic.csv`, which simulates traffic conditions in a futuristic urban environment. Key columns include:

  - `City`: The name of the futuristic city (e.g., Ecoopolis, AquaCity).
  - `Vehicle Type`: The type of vehicle (e.g., Drone, Flying Car, Autonomous Vehicle).
  - `Weather`: Current weather conditions (e.g., Snowy, Solar Flare, Rainy, Clear).
  - `Economic Condition`: Economic state of the city (e.g., Stable, Recession, Booming).
  - `Day Of Week`: Day of the week.
  - `Hour Of Day`: Hour of the day (0-23).
  - `Speed`: Vehicle speed in km/h.
  - `Is Peak Hour`: Binary indicator for peak traffic hours.
  - `Random Event Occurred`: Binary indicator for random events affecting traffic.
  - `Energy Consumption`: Energy consumed by vehicles in kWh.
  - `Traffic Density`: A measure of traffic congestion.


## Technology Stack

The project leverages a modern cloud-native stack:

  - **Frontend/Backend:** [Dash](https://plotly.com/dash/) (Plotly Dash) with [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/) for interactive visualizations and UI.
  - **Data Handling:** [Pandas](https://pandas.pydata.org/) for data loading and manipulation.
  - **Web Server:** [Gunicorn](https://gunicorn.org/) to serve the Dash application.
  - **Containerization:** [Docker](https://www.docker.com/) for packaging the application and its dependencies.
  - **Orchestration:** [Kubernetes](https://kubernetes.io/) (specifically [K3s](https://k3s.io/) for a lightweight cluster) for managing containerized workloads.
  - **Deployment Automation:** [Helm](https://helm.sh/) for templating and deploying Kubernetes manifests.
  - **Ingress Controller:** [Traefik](https://traefik.io/traefik/) for routing external traffic into the Kubernetes cluster.
  - **CI/CD:** [GitHub Actions](https://docs.github.com/en/actions) for automated build, test, and deployment workflows.
  - **Cloud Provider:** Deployed on an **Oracle Cloud Infrastructure (OCI)** instance, demonstrating a hybrid cloud approach where the K3s cluster runs on a self-managed VM.
  - **Large File Storage:** [Git LFS](https://git-lfs.com/) is used to manage the large `futuristic_city_traffic.csv` file within the Git repository.

## Deployment

This dashboard is designed for continuous deployment to a Kubernetes cluster.

### Prerequisites

Before deploying, ensure you have:

1.  **A running Kubernetes cluster:** (e.g., a K3s cluster on an OCI instance).
2.  **`kubectl` configured** to connect to your cluster.
3.  **Helm installed** on your CI/CD runner.
4.  **Traefik Ingress Controller** installed and configured in your cluster (as specified in `values.yaml`).
5.  **A GitHub Personal Access Token (PAT)** with `repo` and `write:packages` scopes for pushing Docker images to GitHub Container Registry (`ghcr.io`). This should be stored as a GitHub Secret (e.g., `CR_PAT`).
6.  **A Kubernetes Secret for `ghcr.io` credentials** in your cluster, named `ghcr-secret`, allowing your pods to pull images from your private GitHub Container Registry.
7.  **A domain** (e.g., `vishvesh.me`) and DNS records configured to point your chosen subdomain (e.g., `citytrafficdash.vishvesh.me`) to the external IP of your Traefik Ingress Controller.

### Kubernetes Configuration

The application is deployed using a Helm chart located in the `dash-chart/` directory. Key configurations are managed via `dash-chart/values.yaml`:

  - **Image:** `ghcr.io/vishvesh11/urban_traffic_density`
  - **Container Port:** `8050` (where Gunicorn serves the Dash app)
  - **Service Type:** `ClusterIP`
  - **Ingress Host:** `citytrafficdash.vishvesh.me` (configurable in `values.yaml`)
  - **Ingress Class:** `traefik`
  - **Health Probes:** Liveness and Readiness probes configured for HTTP GET on `/` at port `8050`, with increased `initialDelaySeconds` and `timeoutSeconds` to accommodate application startup time.

### CI/CD Pipeline

The `build-deploy.yml` GitHub Actions workflow automates the following steps:

1.  **Checkout Code:** Fetches the repository, including Git LFS managed files (`futuristic_city_traffic.csv`).
2.  **Docker Build & Push:** Builds the Docker image based on the `Dockerfile` and pushes it to `ghcr.io` with a unique tag.
3.  **Kubernetes Deployment (Helm):** Performs a `helm upgrade --install` to deploy or update the application on the K3s cluster using the `dash-chart` and the updated image.

## Usage

Once deployed and DNS has propagated, you can access the dashboard at:

`https://citytrafficdash.vishvesh.me/` 

Interact with the dropdowns and the dark mode toggle to explore the traffic data dynamically.

## Local Development

To run the dashboard locally for development or testing:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/vishvesh11/Urban_traffic_density.git
    cd Urban_traffic_density
    ```
2.  **Ensure Git LFS is installed and initialized:**
    ```bash
    git lfs install
    git lfs pull
    ```
    This will download the actual `futuristic_city_traffic.csv` file.
3.  **Create a Python virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate # On Windows: .\venv\Scripts\activate
    ```
4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
5.  **Run the Dash application:**
    ```bash
    gunicorn -b 0.0.0.0:8050 dashboard:server
    ```
6.  Open your browser and navigate to `http://localhost:8050`.



-----
