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
                sh 'rm -r dist || echo '
                sh 'poetry update'
                sh 'poetry version patch'
                sh 'poetry build'
            }
        }
        stage('Upload') {
            steps {
                sh 'echo "${COMMIT_ID}"'
                sh 'poetry run twine upload dist/* || echo'
            }
        }
        stage('Commit version change') {
            steps {
                sh 'echo "${COMMIT_ID}"'
                sh 'git config --global user.email "jenkins@openknowit.com"'
                sh 'git config --global user.name "Jenkins"'
                sh 'git add pyproject.toml'
                sh 'git commit -m "Bump version"'
                sh 'pwd | grep "main" &&  git push origin main'
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
