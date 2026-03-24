
[![CD - on main Push](https://github.com/jacobdvorsky-del/GitHub_Actions_Practice/actions/workflows/cd.yml/badge.svg)](https://github.com/jacobdvorsky-del/GitHub_Actions_Practice/actions/workflows/cd.yml)
[![CI - Pull Request](https://github.com/jacobdvorsky-del/GitHub_Actions_Practice/actions/workflows/ci.yaml/badge.svg)](https://github.com/jacobdvorsky-del/GitHub_Actions_Practice/actions/workflows/ci.yaml)
[![Manual Deploy](https://github.com/jacobdvorsky-del/GitHub_Actions_Practice/actions/workflows/manual-deploy.yml/badge.svg)](https://github.com/jacobdvorsky-del/GitHub_Actions_Practice/actions/workflows/manual-deploy.yml)
# Overview
Main focus of this project was to practice CI/CD Workflows for the application.  
Application is dockerized and uses tagging based on commit sha.

**This project contains:**
- Flask api application: Simple api for storing tasks (title, description)  
- Pytest tests for checking api endpoints

**The Project uses 3 workflows:**
- CI: Runs on every Pull Request to main (Lint, Test, Build)  
- CD: Runs after push to main (Build + Push, Deploy Staging, Run Tests, Deploy Production)
- Manual Deploy: Deploys specific image to Production/Staging (workflow_dispatch)

**Additional Protections:**  
- Approval Gate: Deploy on production environment needs manual approval
- Branch Protection: main branch is protected with rules
  - no direct push to main
  - base branch needs to be up to date with main
  - CI workflow needs to pass
 
# Architecture Diagram:

```mermaid
flowchart LR
    A([Pull Request]) -->  B[CI]
    B --> C{{Lint}}
    C -->D{{Test}} --> F
    C -->E{{Build}} --> F
    F([Merge]) -->
    G[CD] -->
    H{{Build And Push}} --> 
    I{{Deploy Staging}} -->
    J{{Test Staging}} --> 
    K[[Approval Gate]] -->
    L{{Deploy Production}}
```  
  
# Pipeline Description  
**CI:**
- Validates PR branch before merge
- Runs When Pull Request to main is created
- Jobs:
  - Lint: Runs Lint (flake8)
  - Test: Placeholder for future Unit Tests
  - Build: Builds Docker Image (No Push)

**CD:**
- Goal: Build and Deploy application to Production
- Runs When code is pushed to main
- Jobs:
  - Build and Push: Builds image and pushes to ghcr. tags with :latest and :sha
  - Deploy Staging: Deploys image to Staging Environment
  - Tests: Runs Pytest tests against Staging Environment
  - Deploy Production: Requires manual approval, Deploys application to Production environment  

**CD - Manual:**
- Goal: Safety net for fast deployment
- Runs on workflow_dispatch
- Inputs:
  - image-tag: Tag of image to be deployed
  - environment: staging/production
- Jobs:
  - Deploy: Deploys image with tag from input on specified environment.

# Run locally
Project contains docker-compose.yaml to start application with command:
` docker compose up -d `
This starts the container with :latest tag.  
We can run docker compose with specified tag with command ` IMAGE_TAG=<tag> docker compose up -d `

# Deploy flow  
When Code is merged to main, CD pipeline triggers. It builds the image from Dockerfile and adds tags to the image: latest and sha of the commit. Then it pushes the image to ghcr.  
After push deploy to staging job starts. It connects to the VM with ssh and pulls the image, then it stops old container and starts the new one.  
Then the Test job runs. It installs the pytest requirements and runs the tests against staging environment.  
After tests, the production job requires manual trigger to start. After approval, the application is deployed to production the same way as it was deployed on staging.  
If production deploy fails, run Manual Deploy workflow with previous stable sha tag.

# Improvements  
There are few points I would improve:  
- The CI pipeline could have more trigger rules, for example, could be run only when something changes in App project folder and/or Test Folder. I do not like that it is triggered even on small change in README.md file.
- Deployment on staging and production is very similar, I think shared workflow could be used for those jobs. 
- Add automatic rollback in case deploy to production goes wrong, now I only have manual deploy as safety net.
- There is health check on deploy, I would like to use some better solution than sleep as a wait.
- Concurrency is not correctly set between manual and automatic CD, manual CD should stop all automatic CD deploys.