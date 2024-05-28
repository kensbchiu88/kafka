from confluent_kafka.admin import AdminClient

# Kafka broker 配置
conf = {
    'bootstrap.servers': 'localhost:9096',
    'security.protocol': 'SASL_PLAINTEXT',
    'sasl.mechanisms': 'PLAIN',
    'sasl.username': 'redpanda',
    'sasl.password': 'redpandasecret123'
}

# 創建 AdminClient
admin_client = AdminClient(conf)

# 列出主題
def list_topics():
    try:
        # 獲取元數據
        metadata = admin_client.list_topics(timeout=10)
        
        # 列出所有主題
        topics = metadata.topics
        for topic in topics:
            print(topic)
    except Exception as e:
        print(f"Failed to list topics: {e}")

if __name__ == "__main__":
    list_topics()
