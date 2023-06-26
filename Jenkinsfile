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
            when {
                expression {
                    return env.GIT_BRANCH == "origin/main"
                }
            }
            steps {
                sh 'echo "${COMMIT_ID}"'
                sh 'poetry run twine upload dist/* || echo'
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
