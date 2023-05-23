pipeline{
    agent none
    stages{
        stage("Build Selnium Test Image"){
            steps{
                script{
                    app= docker.build("aothmana/selenium-grid-python")
                }
            }
            
        }

        stage("Push Image"){
        steps{
             script{
                docker.withRegistry('https://registry.hub.docker.com','dockerhub'){
                    app.push('${BUILD_NUMBER}')
                    app.push("latest")
                }
             }
            }
        }
        
    }
   
}