---
name: block-storage
description: 管理块存储卷和LVM。配置云块存储和本地磁盘。在管理磁盘存储时使用。
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

# 块存储

管理块存储卷，包括LVM、基于云的EBS、文件系统创建、快照和RAID配置。涵盖从配置原始磁盘到在生产中扩展卷的完整生命周期。

## 何时使用

- 在Linux服务器上添加、分割或格式化新磁盘
- 管理LVM逻辑卷以实现灵活的存储分配
- 配置和连接云块存储（AWS EBS）
- 创建和恢复快照用于备份或迁移
- 为冗余或性能配置软件RAID
- 扩展现有卷而不需要停机

## 先决条件

- 目标系统上的root或sudo访问权限
- 为LVM操作安装了`lvm2`包
- 为软件RAID安装了`mdadm`包
- 为EBS操作配置了AWS CLI
- 了解工作负载的I/O特性（IOPS、吞吐量）

## 磁盘发现和分割

```bash
# 列出所有块设备
lsblk
lsblk -f    # 显示文件系统类型和挂载点

# 显示详细的磁盘信息
fdisk -l /dev/sdb

# 识别磁盘型号和健康状况（需要smartmontools）
smartctl -a /dev/sda
smartctl -H /dev/sda    # 快速健康检查

# 创建GPT分区表和单个分区
parted /dev/sdb mklabel gpt
parted /dev/sdb mkpart primary ext4 0% 100%

# 备选：使用fdisk进行MBR分区
fdisk /dev/sdb
# n -> 新分区, p -> 主分区, Enter默认值, w -> 写入

# 通知内核分区表更改
partprobe /dev/sdb

# 擦除文件系统签名（为LVM或RAID做准备）
wipefs -a /dev/sdb1
```

## 文件系统创建和管理

```bash
# 创建ext4文件系统
mkfs.ext4 /dev/sdb1

# 创建带标签和保留块调整的ext4文件系统
mkfs.ext4 -L appdata -m 1 /dev/sdb1    # 1%保留块（默认为5%）

# 创建XFS文件系统（推荐用于大卷）
mkfs.xfs /dev/sdb1

# 创建带标签的XFS文件系统
mkfs.xfs -L appdata /dev/sdb1

# 挂载文件系统
mkdir -p /data
mount /dev/sdb1 /data

# 添加持久挂载到fstab（使用UUID以提高可靠性）
blkid /dev/sdb1    # 获取UUID
echo 'UUID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx  /data  ext4  defaults,noatime  0  2' >> /etc/fstab

# 挂载fstab中的所有条目
mount -a

# 检查和修复文件系统（首先卸载）
umount /data
fsck.ext4 -y /dev/sdb1
xfs_repair /dev/sdb1    # 对于XFS

# 调整ext4大小（在挂载时可以在线增长）
resize2fs /dev/sdb1

# 调整XFS大小（必须挂载才能增长）
xfs_growfs /data

# 检查文件系统使用情况
df -hT
```

## LVM管理

### 创建LVM堆栈

```bash
# 步骤1：创建物理卷
pvcreate /dev/sdb /dev/sdc

# 查看物理卷
pvs
pvdisplay /dev/sdb

# 步骤2：从物理卷创建卷组
vgcreate data_vg /dev/sdb /dev/sdc

# 查看卷组
vgs
vgdisplay data_vg

# 步骤3：创建逻辑卷
# 固定大小
lvcreate -L 100G -n app_lv data_vg

# 使用自由空间的百分比
lvcreate -l 50%FREE -n logs_lv data_vg

# 使用所有剩余空间
lvcreate -l 100%FREE -n backup_lv data_vg

# 查看逻辑卷
lvs
lvdisplay /dev/data_vg/app_lv

# 步骤4：创建文件系统并挂载
mkfs.ext4 /dev/data_vg/app_lv
mkdir -p /data/app
mount /dev/data_vg/app_lv /data/app

# 添加到fstab
echo '/dev/data_vg/app_lv  /data/app  ext4  defaults,noatime  0  2' >> /etc/fstab
```

### 扩展卷（在线）

```bash
# 扩展逻辑卷20GB
lvextend -L +20G /dev/data_vg/app_lv

# 扩展以填充VG中的所有自由空间
lvextend -l +100%FREE /dev/data_vg/app_lv

# 增长ext4文件系统（在线，无需卸载）
resize2fs /dev/data_vg/app_lv

# 增长XFS文件系统（在线）
xfs_growfs /data/app

# 合并：在一个命令中扩展LV并调整文件系统大小
lvextend -L +20G --resizefs /dev/data_vg/app_lv
```

### 向现有VG添加新磁盘

```bash
# 添加新的物理卷
pvcreate /dev/sdd

# 扩展卷组
vgextend data_vg /dev/sdd

# 现在扩展任何逻辑卷以使用新空间
lvextend -l +100%FREE --resizefs /dev/data_vg/app_lv
```

### LVM快照

```bash
# 创建快照（需要VG中的自由空间）
lvcreate -L 10G -s -n app_snap /dev/data_vg/app_lv

# 以只读方式挂载快照以进行备份
mkdir -p /mnt/snapshot
mount -o ro /dev/data_vg/app_snap /mnt/snapshot

# 从快照执行备份
tar czf /backup/app-$(date +%Y%m%d).tar.gz -C /mnt/snapshot .

# 完成后卸载并删除快照
umount /mnt/snapshot
lvremove -f /dev/data_vg/app_snap

# 从快照恢复（将LV恢复到快照点 -- 破坏性）
lvconvert --merge /dev/data_vg/app_snap
# 注意：如果LV已挂载，合并会在下次激活时发生（重启）
```

### 减少和删除LVM组件

```bash
# 缩小逻辑卷（仅ext4 -- XFS无法缩小）
# 必须首先卸载
umount /data/app
e2fsck -f /dev/data_vg/app_lv
resize2fs /dev/data_vg/app_lv 80G
lvreduce -L 80G /dev/data_vg/app_lv
mount /data/app

# 删除逻辑卷
umount /data/app
lvremove /dev/data_vg/app_lv

# 从卷组中删除磁盘（首先迁移数据）
pvmove /dev/sdc            # 将扩展迁移到其他PV
vgreduce data_vg /dev/sdc  # 从VG中删除PV
pvremove /dev/sdc           # 清理PV元数据
```

## AWS EBS管理

```bash
# 创建gp3卷（通用SSD）
aws ec2 create-volume \
  --availability-zone us-east-1a \
  --size 100 \
  --volume-type gp3 \
  --iops 3000 \
  --throughput 125 \
  --tag-specifications 'ResourceType=volume,Tags=[{Key=Name,Value=app-data},{Key=Environment,Value=production}]'

# 创建io2卷（为数据库配置的IOPS SSD）
aws ec2 create-volume \
  --availability-zone us-east-1a \
  --size 500 \
  --volume-type io2 \
  --iops 10000

# 使用过滤器列出卷
aws ec2 describe-volumes \
  --filters "Name=tag:Environment,Values=production" \
  --query 'Volumes[*].{ID:VolumeId,Size:Size,Type:VolumeType,State:State,AZ:AvailabilityZone}' \
  --output table

# 将卷连接到实例
aws ec2 attach-volume \
  --volume-id vol-0abc123def456789 \
  --instance-id i-0abc123def456789 \
  --device /dev/xvdf

# 连接后，在实例上格式化和挂载
lsblk                               # 识别新设备（例如/dev/nvme1n1）
mkfs.ext4 /dev/nvme1n1
mkdir -p /data
mount /dev/nvme1n1 /data

# 修改卷（调整大小而不分离 -- gp3/io2）
aws ec2 modify-volume \
  --volume-id vol-0abc123def456789 \
  --size 200

# 调整大小后，在实例上增长文件系统
growpart /dev/nvme1n1 1              # 如果分割
resize2fs /dev/nvme1n1               # ext4
# xfs_growfs /data                   # XFS

# 创建快照
aws ec2 create-snapshot \
  --volume-id vol-0abc123def456789 \
  --description "Pre-upgrade snapshot $(date +%Y-%m-%d)" \
  --tag-specifications 'ResourceType=snapshot,Tags=[{Key=Name,Value=pre-upgrade}]'

# 列出快照
aws ec2 describe-snapshots \
  --owner-ids self \
  --query 'Snapshots[*].{ID:SnapshotId,Vol:VolumeId,Size:VolumeSize,Date:StartTime,Desc:Description}' \
  --output table

# 从快照创建卷（用于恢复或迁移）
aws ec2 create-volume \
  --snapshot-id snap-0abc123def456789 \
  --availability-zone us-east-1a \
  --volume-type gp3

# 分离卷
aws ec2 detach-volume --volume-id vol-0abc123def456789

# 删除卷（确保首先分离）
aws ec2 delete-volume --volume-id vol-0abc123def456789
```

## 软件RAID (mdadm)

```bash
# 安装mdadm
apt install -y mdadm    # Debian/Ubuntu
dnf install -y mdadm    # RHEL/CentOS

# 使用2个磁盘创建RAID 1（镜像）
mdadm --create /dev/md0 --level=1 --raid-devices=2 /dev/sdb /dev/sdc

# 使用3个磁盘+ 1个备用创建RAID 5（带奇偶校验的条纹）
mdadm --create /dev/md0 --level=5 --raid-devices=3 --spare-devices=1 /dev/sdb /dev/sdc /dev/sdd /dev/sde

# 使用4个磁盘创建RAID 10（条纹镜像）
mdadm --create /dev/md0 --level=10 --raid-devices=4 /dev/sdb /dev/sdc /dev/sdd /dev/sde

# 检查RAID状态
cat /proc/mdstat
mdadm --detail /dev/md0

# 保存RAID配置（在重启时持续存在）
mdadm --detail --scan >> /etc/mdadm/mdadm.conf     # Debian
mdadm --detail --scan >> /etc/mdadm.conf            # RHEL
update-initramfs -u                                  # Debian

# 在RAID设备上创建文件系统
mkfs.ext4 /dev/md0
mkdir -p /data
mount /dev/md0 /data

# 替换故障磁盘
mdadm --manage /dev/md0 --fail /dev/sdc
mdadm --manage /dev/md0 --remove /dev/sdc
# 插入新磁盘，然后：
mdadm --manage /dev/md0 --add /dev/sdf

# 监控重建进度
watch cat /proc/mdstat

# RAID级别建议：
# RAID 1:  2+磁盘，镜像，适合OS/启动驱动器
# RAID 5:  3+磁盘，单一奇偶校验，良好读取性能
# RAID 6:  4+磁盘，双奇偶校验，可承受2个磁盘故障
# RAID 10: 4+磁盘，镜像条纹，最佳I/O性能
```

## 故障排除

| 症状 | 诊断命令 | 常见修复 |
|---|---|---|
| 磁盘未显示 | `lsblk`、`dmesg \| tail` | 检查物理连接；重新扫描SCSI总线 |
| 文件系统只读 | `dmesg \| grep error`、`mount` | 检测到文件系统错误；卸载后运行`fsck` |
| LVM：VG中无自由空间 | `vgs`、`pvs` | 使用`vgextend`添加新PV |
| EBS卷不可见 | 实例上的`lsblk` | 检查AWS控制台中的连接状态；NVMe命名不同 |
| RAID降级 | `cat /proc/mdstat` | 使用`mdadm --manage --add`替换故障磁盘 |
| 无法调整文件系统大小 | `lvs`、`df -h` | 首先扩展LV，然后调整FS大小；XFS需要挂载 |
| EBS上的I/O缓慢 | `iostat -x 2`、检查卷类型 | 升级到gp3/io2，增加IOPS/吞吐量 |
| 快照耗时太长 | AWS控制台：快照进度 | 快照是增量的；第一个耗时最长 |

## 相关技能

- `linux-administration` -- 磁盘和文件系统基础
- `performance-tuning` -- I/O调度器和fio基准测试
- `nfs-storage` -- 构建在块存储之上的网络文件系统
- `backup-recovery` -- 基于快照和文件级的备份策略
- `object-storage` -- 用于非结构化数据的替代存储模型

## 限制

- 基础设施命令可能会中断服务：在变更状态之前确认目标主机/范围并拥有备份/快照。
- 仅文档导入：上游脚本和模板未捆绑。
