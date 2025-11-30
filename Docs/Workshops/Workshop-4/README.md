# Workshop 4 – CI/CD with GitHub Actions

## General Objective
Implement a CI/CD pipeline that automates compilation, testing, and Docker image building for the project’s microservices. Additionally, organize the repository following the best practices required by the course rubric.

---

# 1. Project Structure

The final structure of Workshop-4 in this repository is:
```
SOFTWARE-ENGINEERING-SEMINAR/
├── .github/
│   └── workflows/
│       └── ci-cd.yml
└── Docs/
    └── Workshops/
        ├── Workshop-3/
        │   ├── auth-service/
        │   │   ├── src/
        │   │   ├── pom.xml
        │   │   ├── Dockerfile
        │   │   └── README.md
        │   └── core-service/
        │       ├── src/
        │       ├── requirements.txt
        │       └── tests/
        └── Workshop-4/
            ├── .github/workflows/
            │   └── ci-cd.yml
            │
            ├── app/
            │   ├── auth-service/
            │   ├── core-service/
            │   ├── docs/
            │   ├── web/
            │   └── docker-composer.yml
            │
            ├── Latex/
            │   ├── Cucumber/
            │   ├── Dockerfiles/
            │   ├── github/
            │   ├── JMeter/
            │   ├── Portada/
            │   ├── main.pdf
            │   ├── main.tex
            │   └── settings.tex
            │
            └── README.md
```