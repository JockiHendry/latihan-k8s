helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo add elastic https://helm.elastic.co
helm install keycloak -f keycloak-values.yaml bitnami/keycloak
helm install mongodb-item-stock -f mongodb-item-stock-values.yaml bitnami/mongodb
helm install rabbitmq -f rabbitmq-values.yaml bitnami/rabbitmq
helm install elasticsearch -f elasticsearch-values.yaml elastic/elasticsearch