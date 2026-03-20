# Overview
Main focus of this project was to practice CI/CD Workflows for the application.  

This project contains:  
- Flask api application: Simple api for storing tasks (title, description)  
- Pytest tests for checking api endpoints

Application is dockerized and uses tagging based on commit sha.

The Project uses 3 workflows:
- CI: Runs on every Pull Request to main (Lint, Test, Build)  
- CD: Runs after push to main (Build + Push, Deploy Staging, Run Tests, Deploy Production)
- Manual Deploy: Deploys specific image to Production/Staging (workflow_dispatch)

Additional Protections:  
- Approval Gate: Deploy on production environment needs manual approval
- Branch Protection: main branch is protected with rules
  - no direct push to main
  - base branch needs to be up to date with main
  - CI workflow needs to pass
 
# Architecture Diagram:
 PR -> CI (Lint -> Test -> Build) -> Merge -> CD (Build and Push -> Deploy Staging -> Test Staging -> Deploy Production)

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