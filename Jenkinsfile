@Library("Shared") _
pipeline {
    agent { label "ghost"}
    stages {
        stage("Code"){
            steps{
                script{
                    code_clone("https://github.com/AkashSrivastava1805/llama-parser.git","main")
                }
            }
        }
        stage("Build"){
            steps{
                script{
                    docker_build("officialakashsrivastava","llama-parser","V1.0")
                }
            }
        }
        stage("Pushing to Docker Hub"){
            steps{
                script{
                    pushing_to_docker_hub("officialakashsrivastava","llama-parser","V1.0")
                }
            }
        }
        stage("Deploy"){
            steps{
                echo "Delpoying the code"
                sh """
                    sudo docker stop llama-parser || true
                    sudo docker rm llama-parser || true
                    sudo docker run -d --name llama-parser -p 8501:8501 officialakashsrivastava/llama-parser:V1.0
                """
                echo "Code deployed"
            }
        }
    }
}
