# airflow test

> apache airflow de testes.

> yaml do docker-compose: <a href="https://airflow.apache.org/docs/apache-airflow/2.9.1/docker-compose.yaml" target="_blank">docker-compose.yaml</a>

## 💻 Pré-requisitos

Antes de começar, atente-se aos seguintes requisitos:

- criar bucket: <b>mvs-sync</b> e essa estrutura de pastas: <b>input/disney/character/</b>

- Para <b>Airflow local</b> -> acrescentar uma chave no Airflow.
  1. Admin -> Connections -> Add a new record
  2. Connection Id = aws_default<br>
     Connection Type = Amazon Web Services<br>
     AWS Access Key ID = <i><your_aws_key></i><br>
     AWS Secret Access Key = <i><your_aws_access_key></i><br>

- Para <b>Airflow gerenciado</b> da AWS (MWAA).
  1. criar policy de acesso ao bucket S3: <b>mvs-sync</b> com as permissões: <b>ListBucket</b>, <b>GetObject</b> e <b>PutObject</b>
  2. em seguida, criar uma nova role e associar com a policy.
  3. depois, acrescentar a role na aba permissions do Airflow MWAA no console da AWS.
