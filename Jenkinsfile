pipeline {
    agent any

    environment {
        IMAGE = "chanhengmenh/assignment-7-api:latest"
    }

    stages {

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE ./app'
            }
        }

        stage('Push Image') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'USER',
                    passwordVariable: 'PASS'
                )]) {
                    sh 'echo "Logging into Docker..."'
                    sh 'echo $PASS | docker login -u $USER --password-stdin'
                    sh 'docker push $IMAGE'
                }
            }
        }

        stage('Provision EC2') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'aws-creds'
                ]]) {
                    dir('terraform') {
                        sh 'terraform init'
                        sh 'terraform apply -auto-approve'
                    }
                }
            }
        }

        stage('Deploy App') {
            steps {
                script {
                    def ip = sh(
                        script: "cd terraform && terraform output -raw public_ip",
                        returnStdout: true
                    ).trim()

                    withCredentials([sshUserPrivateKey(
                        credentialsId: 'ec2-key',
                        keyFileVariable: 'KEY'
                    )]) {

                        sh """
                        ssh -i $KEY -o StrictHostKeyChecking=no ubuntu@${ip} '
                            sudo docker pull $IMAGE &&
                            sudo docker stop assignment-7 || true &&
                            sudo docker rm assignment-7 || true &&
                            sudo docker run -d -p 8000:8000 --restart always --name assignment-7 $IMAGE
                        '
                        """
                    }
                }
            }
        }
    }
}