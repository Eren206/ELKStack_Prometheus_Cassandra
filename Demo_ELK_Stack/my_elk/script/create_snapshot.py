import requests
import datetime

# Elasticsearch configuration
ES_HOST = "http://localhost:9200"  # Địa chỉ Elasticsearch
USERNAME = "elastic"               # Tên người dùng
PASSWORD = "myelasticpass"          # Mật khẩu
REPO_NAME = "repo"            # Tên repository
SNAPSHOT_NAME = f"snapshot_byscript_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"  # Tên snapshot
HEADERS = {"Content-Type": "application/json"}

def create_repository():
    """
    Tạo repository cho snapshot nếu chưa tồn tại.
    """
    repo_settings = {
        "type": "fs",  # Loại repository (fs: file system)
        "settings": {
            "location": "/usr/share/elasticsearch/backup",  # Mount path trong container Docker
            "compress": True  # Bật nén dữ liệu snapshot
        }
    }
    response = requests.put(
        f"{ES_HOST}/_snapshot/{REPO_NAME}", 
        json=repo_settings, 
        headers=HEADERS, 
        auth=(USERNAME, PASSWORD)
    )
    if response.status_code in [200, 201]:
        print("Repository created successfully!")
    elif response.status_code == 400 and "already exists" in response.text:
        print("Repository already exists.")
    else:
        print(f"Failed to create repository: {response.text}")

def create_snapshot():
    """
    Tạo snapshot với các cài đặt tùy chọn.
    """
    snapshot_settings = {
        "indices": "_all",                 # Snapshot tất cả chỉ mục và data streams
        "ignore_unavailable": True,        # Bỏ qua chỉ mục không khả dụng
        "include_global_state": True,      # Bao gồm trạng thái toàn cầu của cluster
        "partial": False,                  # Không cho phép snapshot chỉ mục một phần
        "feature_states": ["security", "ml"]  # Sao lưu các tính năng bảo mật và machine learning
    }
    response = requests.put(
        f"{ES_HOST}/_snapshot/{REPO_NAME}/{SNAPSHOT_NAME}?wait_for_completion=true",
        json=snapshot_settings,
        headers=HEADERS,
        auth=(USERNAME, PASSWORD)
    )
    if response.status_code == 200:
        print(f"Snapshot {SNAPSHOT_NAME} created successfully!")
    else:
        print(f"Failed to create snapshot: {response.text}")

def main():
    """
    Quá trình snapshot tự động.
    """
    print("Starting Elasticsearch snapshot process...")
    create_repository()
    create_snapshot()

if __name__ == "__main__":
    main()
