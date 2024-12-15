# I worked on a local minikube cluster

## To create two users; admin-user and developer-user:
# I generated Private Keys
openssl genrsa -out developer.key 2048

openssl genrsa -out admin.key 2048

# Created Certificate Signing Requests (CSRs)
openssl req -new -key developer.key -out developer.csr -subj "/CN=developer-user"

openssl req -new -key admin.key -out admin.csr -subj "/CN=admin-user"

# Signed the CSRs with Minikube's Kubernetes CA
openssl x509 -req -in developer.csr -CA ~/.minikube/ca.crt -CAkey ~/.minikube/ca.key -CAcreateserial -out developer.crt -days 365

openssl x509 -req -in admin.csr -CA ~/.minikube/ca.crt -CAkey ~/.minikube/ca.key -CAcreateserial -out admin.crt -days 365

# Added Users to the Kubeconfig File
kubectl config set-credentials developer-user \
  --client-certificate=developer.crt \
  --client-key=developer.key \
  --embed-certs=true

kubectl config set-credentials admin-user \
  --client-certificate=admin.crt \
  --client-key=admin.key \
  --embed-certs=true

# Created Contexts for Each User
kubectl config set-context developer-context \
  --cluster=minikube \
  --namespace=staging \
  --user=developer-user

kubectl config set-context admin-context \
  --cluster=minikube \
  --user=admin-user


# I created the RDS; mysql database in my AWS consol in the eu-central-1 region where I made sure I had 3 subnets in different AZs, and created an initial database; staging_db in the process. Then, I created an Internet Gateway to allow access into the mysql database to which I enabled public access. I also configured the security group of the VPC to allow inbound traffic of type MYSQL/Aurora on port 3306. After creation;

mysql -h <database-endpoint> -u admin -p

CREATE DATABASE production_db;


# Applied all configuration files for rbac and secret
kubectl apply -f all-config-files


# Set environmental variables for staging environment
export DB_ENDPOINT="database-1.cr3rl632szha.eu-central-1.rds.amazonaws.com"

export DB_USERNAME="admin"

export DB_PASSWORD="Grock5kkkk"

export DB_NAME="staging_db"


# run test-db-connection.py
python3.8 test-db-connection.py

Connecting to database: staging_db
Endpoint: database-1.cr3rl632szha.eu-central-1.rds.amazonaws.com, Username: admin
Connection successful!
Connected to MySQL Server version: 8.0.39
You're connected to database: staging_db
Database connection closed.

# Set environmental variables for production environment
export DB_ENDPOINT="database-1.cr3rl632szha.eu-central-1.rds.amazonaws.com"

export DB_USERNAME="admin"

export DB_PASSWORD="Grock5kkkk"

export DB_NAME="production_db"

# run test-db-connection.py
python3.8 test-db-connection.py

Connecting to database: production_db
Endpoint: database-1.cr3rl632szha.eu-central-1.rds.amazonaws.com, Username: admin
Connection successful!
Connected to MySQL Server version: 8.0.39
You're connected to database: production_db
Database connection closed.


# deploy app in staging environment

kubectl apply -f staging-deploy.yaml

staging-app-86f7c9f895-nzxpc          1/1          Running           0              31s

# deploy app in production environment

kubectl get pods -n production

production-app-84955d7c45-v4w2x         1/1           Running         0                26s