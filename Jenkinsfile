pipeline{
    agent any
    environment {
        PATH="/usr/local/bin/:${env.PATH}"
        CFN_KEYPAIR="the-doctor"
        AWS_REGION = "us-east-1"
        FQDN = "post.mehmetafsar.com"
        DOMAIN_NAME = "mehmetafsar.com"
        GIT_FOLDER = sh(script:'echo ${GIT_URL} | sed "s/.*\\///;s/.git$//"', returnStdout:true).trim()
    }
    stages{
        stage('Setup terraform ansible  binaries') {
            steps {
              script {

                println "Setup teraform ansible  binaries..."
                sh """
                  sudo yum install -y yum-utils
                  sudo yum-config-manager --add-repo https://rpm.releases.hashicorp.com/AmazonLinux/hashicorp.repo
                  sudo yum -y install terraform
                  pip3 install --user ansible
                  pip3 install --user boto3 botocore
                  sudo yum install python-boto3 -y
                """
              }
            }
        } 

        stage('get-keypair'){
            agent any
            steps{
                sh '''
                    if [ -f "${CFN_KEYPAIR}.pem" ]
                    then 
                        echo "file exists..."
                    else
                        aws ec2 create-key-pair \
                          --region ${AWS_REGION} \
                          --key-name ${CFN_KEYPAIR} \
                          --query KeyMaterial \
                          --output text > ${CFN_KEYPAIR}.pem

                        chmod 400 ${CFN_KEYPAIR}.pem

                        ssh-keygen -y -f ${CFN_KEYPAIR}.pem >> the_doctor_public.pem
                    fi
                '''                
            }
        }

        stage('create infrastructure with terraform'){
            agent any
            steps{
                withAWS(credentials: 'mycredentials', region: 'us-east-1') {
                    sh "terraform init" 
                    sh "terraform apply -input=false -auto-approve"
                }    
            }
        }

        stage('Control the nodejs instance') {
            steps {
                echo 'Control the  postgresql instance'
            script {
                while(true) {
                        
                        echo "NOdejs is not UP and running yet. Will try to reach again after 10 seconds..."
                        sleep(10)

                        ip = sh(script:'aws ec2 describe-instances --region ${AWS_REGION} --filters Name=tag-value,Values=ansible_nodejs  --query Reservations[*].Instances[*].[PublicDnsName] --output text | sed "s/\\s*None\\s*//g"', returnStdout:true).trim()

                        if (ip.length() >= 7) {
                            echo "Nodejs Public Ip Address Found: $ip"
                            env.NODEJS_INSTANCE_PUBLIC_DNS = "$ip"
                            sleep(15)
                            break
                        }
                    }
                }
            }
        }

        stage('Control the  postgresql instance') {
            steps {
                echo 'Control the  postgresql instance'
            script {
                while(true) {
                        
                        echo "Postgresql is not UP and running yet. Will try to reach again after 10 seconds..."
                        sleep(10)

                        ip = sh(script:'aws ec2 describe-instances --region ${AWS_REGION} --filters Name=tag-value,Values=ansible_postgresql  --query Reservations[*].Instances[*].[PrivateDnsName] --output text | sed "s/\\s*None\\s*//g"', returnStdout:true).trim()

                        if (ip.length() >= 7) {
                            echo "Postgresql Private Ip Address Found: $ip"
                            env.POSTGRESQL_INSTANCE_PRİVATE_DNS = "$ip"
                            sleep(15)
                            break
                        }
                    }
                }
            }
        }

        stage('dns-record-control'){
            agent any
            steps{
                withAWS(credentials: 'mycredentials', region: 'us-east-1') {
                    script {
                        
                        env.ZONE_ID = sh(script:"aws route53 list-hosted-zones-by-name --dns-name $DOMAIN_NAME --query HostedZones[].Id --output text | cut -d/ -f3", returnStdout:true).trim()
                        env.ELB_DNS = sh(script:"aws route53 list-resource-record-sets --hosted-zone-id $ZONE_ID --query \"ResourceRecordSets[?Name == '\$FQDN.']\" --output text | tail -n 1 | cut -f2", returnStdout:true).trim()  
                    }
                    sh "sed -i 's|{{DNS}}|$ELB_DNS|g' deleterecord.json"
                    sh "sed -i 's|{{FQDN}}|$FQDN|g' deleterecord.json"
                    sh '''
                        RecordSet=$(aws route53 list-resource-record-sets --hosted-zone-id $ZONE_ID --query \"ResourceRecordSets[?Name == '\$FQDN.']\" --output text | tail -n 1 | cut -f2) || true
                        if [ "$RecordSet" != '' ]
                        then
                            aws route53 change-resource-record-sets --hosted-zone-id $ZONE_ID --change-batch file://deleterecord.json
                        
                        fi
                    '''
                    
                }                  
            }
        }

        stage('dns-record'){
            agent any
            steps{
                withAWS(credentials: 'mycredentials', region: 'us-east-1') {
                    script {
                        env.ELB_DNS = sh(script:'aws ec2 describe-instances --region ${AWS_REGION} --filters Name=tag-value,Values=ansible_react  --query Reservations[*].Instances[*].[PublicIpAddress] --output text | sed "s/\\s*None\\s*//g"', returnStdout:true).trim()
                        env.ZONE_ID = sh(script:"aws route53 list-hosted-zones-by-name --dns-name $DOMAIN_NAME --query HostedZones[].Id --output text | cut -d/ -f3", returnStdout:true).trim()   
                    }
                    sh "sed -i 's|{{DNS}}|$ELB_DNS|g' dnsrecord.json"
                    sh "sed -i 's|{{FQDN}}|$FQDN|g' dnsrecord.json"
                    sh "aws route53 change-resource-record-sets --hosted-zone-id $ZONE_ID --change-batch file://dnsrecord.json"
                    
                }                  
            }
        }
  
        stage('Setting up  configuration with ansible') {
            steps {
                echo "Setting up  configuration with ansible"
                sh "sed -i 's|{{key_pair}}|deneme.pem|g' ansible.cfg"
                sh "sed -i 's|{{nodejs_dns_name}}|$NODEJS_INSTANCE_PUBLIC_DNS|g' todo-app-pern/client/.env"
                sh "sed -i 's|{{postgresql_internal_private_dns}}|$POSTGRESQL_INSTANCE_PRİVATE_DNS|g' todo-app-pern/server/.env"
                sh "sed -i 's|{{workspace}}|${WORKSPACE}|g' docker_project.yml"
                sh "sudo ansible-playbook docker_project.yml"
            }
        }
    
    }
    post { 
        success {
            echo "You are Greattt...You can visit https://$FQDN"
        }
    }
}

