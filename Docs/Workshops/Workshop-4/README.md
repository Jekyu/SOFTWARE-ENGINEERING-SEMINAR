# Workshop 4 – CI/CD with GitHub Actions

## General Objective
Implement a CI/CD pipeline that automates compilation, testing, and Docker image building for the project’s microservices. Additionally, organize the repository following the best practices required by the course rubric.

---

# 1. Project Structure

The final structure of Workshop-4 in this repository is:
SOFTWARE-ENGINEERING-SEMINAR/
├── .github/
│ └── workflows/
│ └── ci-cd.yml
└── Docs/
└── Workshops/
├── Workshop-3/
│ ├── auth-service/
│ │ ├── src/
│ │ ├── pom.xml
│ │ ├── Dockerfile
│ │ └── README.md
│ └── core-service/
│ ├── src/
│ ├── requirements.txt
│ └── tests/
└── Workshop-4/
├── .github/workflows/
│ └── ci-cd.yml # Main CI/CD workflow
│
├── app/
│ ├── auth-service/ # Java backend microservice (Spring Boot)
│ ├── core-service/ # Python backend microservice
│ ├── docs/ # Technical documentation
│ ├── web/ # Web or UI documentation
│ └── docker-composer.yml # Local Docker orchestration
│
├── Latex/
│ ├── Cucumber/ # BDD feature and step files
│ ├── Dockerfiles/ # Docker-related LaTeX resources
│ ├── github/ # GitHub Actions evidence
│ ├── JMeter/ # Load testing resources
│ ├── Portada/ # Report cover
│ ├── main.pdf # Final PDF report
│ ├── main.tex # Main LaTeX document
│ └── settings.tex
│
└── README.md # Main documentation for Workshop 4