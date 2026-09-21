pipeline {
    agent any

    environment {
        IMAGE = "your-registry/enterprise-agentic-ai:${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps { checkout scm }
        }

        stage('Install') {
            steps { sh 'python -m pip install -r requirements.txt' }
        }

        stage('Lint') {
            steps { sh 'ruff check .' }
        }

        stage('Test') {
            steps { sh 'pytest -q' }
        }

        stage('Build') {
            steps { sh 'docker build -t $IMAGE .' }
        }

        stage('Push') {
            when { branch 'main' }
            steps {
                // Configure registry credentials in Jenkins.
                sh 'echo "docker push $IMAGE"'
            }
        }

        stage('Deploy') {
            when { branch 'main' }
            steps {
                // Configure kubeconfig/credentials in Jenkins.
                sh 'echo "kubectl set image deployment/enterprise-agentic-ai api=$IMAGE"'
            }
        }
    }
}
