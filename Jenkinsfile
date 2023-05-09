pipeline {
    agent any

    stages {
        stage('Set Commit ID') {
            steps {
                script {
                    env.COMMIT_ID = sh(returnStdout: true, script: 'git rev-parse HEAD').trim()
                    echo "Current commit ID is: ${env.COMMIT_ID}"
                }
            }
        }
        stage('Build') {
            steps {
                sh 'echo "${COMMIT_ID}"'
                sh 'pip install poetry'
                sh 'rm -r dist'
                sh 'poetry build'
            }
        }
        stage('Upload') {
            steps {
                sh 'echo "${COMMIT_ID}"'
                sh 'poetry run twine upload dist/*'
            }
        }
    }

    post {
        success {
            echo 'Build succeeded!'
        }
        failure {
            echo 'Build failed!'
        }
    }
}

