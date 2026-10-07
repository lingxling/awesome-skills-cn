---
name: gcp-cloud-sql
description: 配置Cloud SQL和Spanner数据库。配置高可用性、备份和安全性。在GCP上部署托管数据库时使用。
category: devops
risk: critical
source: https://github.com/BagelHole/DevOps-Security-Agent-Skills
source_repo: BagelHole/DevOps-Security-Agent-Skills
source_type: community
date_added: '2026-09-20'
license: MIT
license_source: https://github.com/BagelHole/DevOps-Security-Agent-Skills/blob/main/LICENSE
compatibility: 需要相关的OS/平台工具和注明的特权访问。仅文档；辅助脚本和模板未捆绑。
metadata:
  author: devops-skills
  version: '1.0'
---

# GCP Cloud SQL

在Google Cloud上部署和管理完全托管的关系数据库（PostgreSQL、MySQL、SQL Server）。

## 何时使用

- 运行生产关系数据库，无需管理复制、修补或备份
- 将本地PostgreSQL或MySQL工作负载迁移到托管服务
- 需要ACID事务、关系架构和SQL查询支持的应用程序
- 需要自动高可用性和区域故障转移的工作负载

## 先决条件

- Google Cloud SDK (`gcloud`) 已安装并已认证
- Cloud SQL Admin API和Service Networking API已启用
- IAM角色`roles/cloudsql.admin`用于完整管理

```bash
gcloud services enable sqladmin.googleapis.com servicenetworking.googleapis.com
```

## 实例层级参考

| 层级 | vCPUs | 内存 | 用例 |
|------|-------|--------|----------|
| db-f1-micro | 共享 | 0.6 GB | 仅开发/测试 |
| db-g1-small | 共享 | 1.7 GB | 低流量暂存 |
| db-custom-2-8192 | 2 | 8 GB | 小生产 |
| db-custom-4-16384 | 4 | 16 GB | 中等生产 |
| db-custom-8-32768 | 8 | 32 GB | 高流量生产 |

## 创建PostgreSQL实例

```bash
gcloud sql instances create prod-db \
  --database-version=POSTGRES_16 \
  --tier=db-custom-4-16384 \
  --region=us-central1 \
  --availability-type=REGIONAL \
  --storage-type=SSD --storage-size=100GB --storage-auto-increase \
  --backup-start-time=02:00 --enable-point-in-time-recovery \
  --retained-backups-count=14 \
  --maintenance-window-day=SUN --maintenance-window-hour=4 \
  --database-flags=max_connections=200,log_min_duration_statement=1000 \
  --root-password=$(openssl rand -base64 24) \
  --labels=env=production,team=backend

gcloud sql databases create myapp --instance=prod-db --charset=UTF8
gcloud sql users create appuser --instance=prod-db \
  --password=$(openssl rand -base64 24)
```

## 创建MySQL实例

```bash
gcloud sql instances create mysql-prod \
  --database-version=MYSQL_8_0 \
  --tier=db-custom-4-16384 --region=us-central1 \
  --availability-type=REGIONAL \
  --storage-type=SSD --storage-size=100GB --storage-auto-increase \
  --backup-start-time=02:00 --enable-bin-log --retained-backups-count=14 \
  --database-flags=slow_query_log=on,long_query_time=2,max_connections=500 \
  --root-password=$(openssl rand -base64 24)
```

## 私有IP配置

```bash
# 分配IP范围并创建私有连接
gcloud compute addresses create google-managed-services \
  --global --purpose=VPC_PEERING --prefix-length=16 --network=my-vpc

gcloud services vpc-peerings connect \
  --service=servicenetworking.googleapis.com \
  --ranges=google-managed-services --network=my-vpc

# 使用私有IP创建实例
gcloud sql instances create private-db \
  --database-version=POSTGRES_16 --tier=db-custom-2-8192 \
  --region=us-central1 \
  --network=projects/${PROJECT_ID}/global/networks/my-vpc \
  --no-assign-ip --availability-type=REGIONAL \
  --storage-type=SSD --storage-size=50GB --storage-auto-increase
```

## 读取副本

```bash
# 同一区域副本
gcloud sql instances create prod-db-replica-1 \
  --master-instance-name=prod-db --tier=db-custom-4-16384 \
  --region=us-central1 --availability-type=ZONAL

# 跨区域副本用于灾难恢复
gcloud sql instances create prod-db-replica-eu \
  --master-instance-name=prod-db --tier=db-custom-4-16384 \
  --region=europe-west1 --availability-type=ZONAL

# 将副本升级为独立版本（灾难恢复）
gcloud sql instances promote-replica prod-db-replica-eu
```

## 备份和恢复

```bash
gcloud sql backups create --instance=prod-db --description="pre-migration"
gcloud sql backups list --instance=prod-db

# 特定时间点恢复
gcloud sql instances clone prod-db prod-db-pitr \
  --point-in-time="2026-03-23T10:00:00Z"

# 导出/导入
gcloud sql export sql prod-db gs://my-bucket/export.sql.gz --database=myapp
gcloud sql import sql prod-db gs://my-bucket/export.sql.gz --database=myapp
```

## Cloud SQL Auth Proxy

```bash
curl -o cloud-sql-proxy \
  https://storage.googleapis.com/cloud-sql-connectors/cloud-sql-proxy/v2.11.0/cloud-sql-proxy.linux.amd64
chmod +x cloud-sql-proxy

./cloud-sql-proxy ${PROJECT_ID}:us-central1:prod-db --port=5432 --auto-iam-authn

# Unix套接字（用于Kubernetes sidecar模式）
./cloud-sql-proxy ${PROJECT_ID}:us-central1:prod-db --unix-socket=/tmp/cloudsql
psql "host=/tmp/cloudsql/${PROJECT_ID}:us-central1:prod-db user=appuser dbname=myapp"
```

## 连接方法摘要

| 方法 | 用例 | 要求 |
|--------|----------|-------------|
| 公共IP + SSL | 开发/测试访问 | 已配置授权网络 |
| Cloud SQL Auth Proxy | GCE/GKE上的生产 | SA与`roles/cloudsql.client` |
| 私有IP | VPC原生应用 | 已配置VPC对等互连 |
| Cloud SQL Connector库 | 应用级集成 | SA凭据 |

## Terraform配置

```hcl
resource "google_sql_database_instance" "main" {
  name             = "prod-db"
  database_version = "POSTGRES_16"
  region           = "us-central1"

  settings {
    tier              = "db-custom-4-16384"
    availability_type = "REGIONAL"
    disk_type         = "PD_SSD"
    disk_size         = 100
    disk_autoresize   = true

    backup_configuration {
      enabled                        = true
      start_time                     = "02:00"
      point_in_time_recovery_enabled = true
      backup_retention_settings { retained_backups = 14 }
    }

    ip_configuration {
      ipv4_enabled    = false
      private_network = google_compute_network.vpc.id
      require_ssl     = true
    }

    maintenance_window { day = 7; hour = 4 }
    database_flags { name = "max_connections"; value = "200" }

    user_labels = { env = "production" }
  }

  deletion_protection = true
  depends_on          = [google_service_networking_connection.private_vpc]
}

resource "google_sql_database" "app" {
  name     = "myapp"
  instance = google_sql_database_instance.main.name
}

resource "google_sql_user" "app" {
  name     = "appuser"
  instance = google_sql_database_instance.main.name
  password = random_password.db_password.result
}

resource "google_sql_database_instance" "replica" {
  name                 = "prod-db-replica-1"
  master_instance_name = google_sql_database_instance.main.name
  region               = "us-central1"
  database_version     = "POSTGRES_16"

  replica_configuration { failover_target = false }

  settings {
    tier            = "db-custom-4-16384"
    disk_type       = "PD_SSD"
    disk_autoresize = true
    ip_configuration {
      ipv4_enabled    = false
      private_network = google_compute_network.vpc.id
    }
  }
}

resource "google_compute_global_address" "private_ip" {
  name          = "google-managed-services"
  purpose       = "VPC_PEERING"
  address_type  = "INTERNAL"
  prefix_length = 16
  network       = google_compute_network.vpc.id
}

resource "google_service_networking_connection" "private_vpc" {
  network                 = google_compute_network.vpc.id
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.private_ip.name]
}
```

## 常见操作

```bash
gcloud sql instances list
gcloud sql instances describe prod-db \
  --format="yaml(state,settings.tier,settings.availabilityType,ipAddresses)"
gcloud sql instances patch prod-db --storage-size=200GB
gcloud sql instances patch prod-db --database-flags=max_connections=300
gcloud sql instances restart prod-db
```

## 故障排除

| 症状 | 原因 | 解决方案 |
|---------|-------|-----|
| 通过公共IP`Connection refused` | IP不在授权网络中 | 使用`gcloud sql instances patch --authorized-networks`添加IP |
| `SSL required`错误 | `require_ssl=true`但客户端不使用SSL | 使用Cloud SQL Proxy或传递`sslmode=require` |
| 高复制延迟 | 副本层级太小或主副本写入量过大 | 增加副本层级；减少写入负载 |
| 实例缓慢，尽管RUNNABLE | CPU/内存配置不足 | 使用`gcloud sql instances patch --tier`缩放层级 |
| Proxy返回`ECONNREFUSED` | 错误的连接名称或缺少IAM角色 | 验证`project:region:instance`格式；授予`roles/cloudsql.client` |
| 无法创建私有IP实例 | VPC对等互连未建立 | 首先运行`gcloud services vpc-peerings connect` |
| 备份恢复失败 | 版本不兼容 | 确保源和目标之间的主要数据库版本相同 |

## 相关技能

- **gcp-networking** - 用于Cloud SQL私有IP的VPC和私有服务连接
- **terraform-gcp** - 使用基础设施即代码配置Cloud SQL
- **gcp-gke** - 通过sidecar代理将Kubernetes工作负载连接到Cloud SQL
- **gcp-compute** - 在连接到Cloud SQL的Compute Engine上运行应用程序

## 限制

- 基础设施命令可能会中断服务：在变更状态之前确认目标主机/范围并拥有备份/快照。
- 仅文档导入：上游脚本和模板未捆绑。
