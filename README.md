# airflow test

> apache airflow de testes.

> yaml do docker-compose: https://airflow.apache.org/docs/apache-airflow/2.9.1/docker-compose.yaml

## 💻 Pré-requisitos

Antes de começar, atente-se aos seguintes requisitos:

- criar bucket: mvs-sync e essa estrutura de pastas: input/disney/character/

- Para Airflow local -> acrescentar uma chave no Airflow.
  1. Admin -> Connections -> Add a new record
  2. Connection Id = aws_default
     Connection Type = Amazon Web Services
     AWS Access Key ID = <your_aws_key>
     AWS Secret Access Key = <your_aws_access_key>

- Para Airflow gerenciado da AWS (MWAA).
  1. criar policy de acesso ao bucket S3 com as permissões: ListBucket, GetObject e PutObject
  2. em seguida, criar uma nova role e associar com a policy.
  3. depois, acrescentar a role na aba permissions do Airflow MWAA no console da AWS.
