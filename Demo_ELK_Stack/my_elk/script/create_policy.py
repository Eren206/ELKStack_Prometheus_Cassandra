import requests
import json

# Cấu hình Elasticsearch
ES_HOST = "http://localhost:9200"  # URL Elasticsearch
USERNAME = "elastic"               # Tên người dùng Elasticsearch
PASSWORD = "myelasticpass"          # Mật khẩu
POLICY_NAME = "daily-snapshot-policy_script"  # Tên policy snapshot
REPO_NAME = "repo"            # Repository cho snapshot
HEADERS = {"Content-Type": "application/json"}

def create_snapshot_policy():
    """
    Tạo snapshot lifecycle policy.
    """
    policy_settings = {
        "schedule": "0 0 2 * * ?",  # Lịch trình chạy snapshot: 2 giờ sáng mỗi ngày (cron)
        "name": "<daily-script-{now/d}>",  # Tên snapshot tự động (dựa trên ngày hiện tại)
        "repository": REPO_NAME,    # Tên repository
        "config": {
            "indices": ["test"],  # Chỉ mục hoặc mẫu chỉ mục cần sao lưu
            "ignore_unavailable": True,
            "include_global_state": False,
            "partial": False
        },
        "retention": {  # Chính sách lưu giữ snapshot
            "expire_after": "30d"  # Xóa snapshot sau 30 ngày
        }
    }
    # Gọi API Elasticsearch để tạo policy
    response = requests.put(
        f"{ES_HOST}/_slm/policy/{POLICY_NAME}",
        auth=(USERNAME, PASSWORD),
        headers=HEADERS,
        data=json.dumps(policy_settings)
    )
    # Kiểm tra kết quả
    if response.status_code in [200, 201]:
        print(f"[SUCCESS] Snapshot policy '{POLICY_NAME}' đã được tạo thành công!")
    else:
        print(f"[ERROR] Không thể tạo snapshot policy '{POLICY_NAME}'.")
        print(f"Chi tiết lỗi: {response.status_code} - {response.text}")

def main():
    print("Creating snapshot lifecycle policy...")
    create_snapshot_policy()

if __name__ == "__main__":
    main()
