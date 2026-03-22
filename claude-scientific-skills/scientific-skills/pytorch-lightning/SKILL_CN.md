---
name: pytorch-lightning
description: 深度学习框架（PyTorch Lightning）。将PyTorch代码组织为LightningModules，配置Trainer用于多GPU/TPU，实现数据管道、回调、日志记录（W&B、TensorBoard）、分布式训练（DDP、FSDP、DeepSpeed），用于可扩展的神经网络训练。
license: Apache-2.0 license
metadata:
    skill-author: K-Dense Inc.
---

# PyTorch Lightning

## 概述

PyTorch Lightning是一个深度学习框架，它组织PyTorch代码以消除样板代码，同时保持完全的灵活性。自动化训练工作流、多设备编排，并实现神经网络训练和跨多个GPU/TPU扩展的最佳实践。

## 使用场景

当您需要以下操作时使用此技能：
- 使用PyTorch Lightning构建、训练或部署神经网络
- 将PyTorch代码组织为LightningModules
- 配置Trainer用于多GPU/TPU训练
- 使用LightningDataModules实现数据管道
- 使用回调、日志记录和分布式训练策略（DDP、FSDP、DeepSpeed）
- 专业地构建深度学习项目

## 核心功能

### 1. LightningModule - 模型定义

将PyTorch模型组织为六个逻辑部分：

1. **初始化** - `__init__()` 和 `setup()`
2. **训练循环** - `training_step(batch, batch_idx)`
3. **验证循环** - `validation_step(batch, batch_idx)`
4. **测试循环** - `test_step(batch, batch_idx)`
5. **预测** - `predict_step(batch, batch_idx)`
6. **优化器配置** - `configure_optimizers()`

**快速模板参考：** 请参见`scripts/template_lightning_module.py`获取完整的样板代码。

**详细文档：** 阅读`references/lightning_module.md`获取综合方法文档、钩子、属性和最佳实践。

### 2. Trainer - 训练自动化

Trainer自动化训练循环、设备管理、梯度操作和回调。关键功能：

- 多GPU/TPU支持，带有策略选择（DDP、FSDP、DeepSpeed）
- 自动混合精度训练
- 梯度累积和裁剪
- 检查点和早停
- 进度条和日志记录

**快速设置参考：** 请参见`scripts/quick_trainer_setup.py`获取常见的Trainer配置。

**详细文档：** 阅读`references/trainer.md`获取所有参数、方法和配置选项。

### 3. LightningDataModule - 数据管道组织

在可重用的类中封装所有数据处理步骤：

1. `prepare_data()` - 下载和处理数据（单进程）
2. `setup()` - 创建数据集并应用转换（每个GPU）
3. `train_dataloader()` - 返回训练DataLoader
4. `val_dataloader()` - 返回验证DataLoader
5. `test_dataloader()` - 返回测试DataLoader

**快速模板参考：** 请参见`scripts/template_datamodule.py`获取完整的样板代码。

**详细文档：** 阅读`references/data_module.md`获取方法详情和使用模式。

### 4. Callbacks - 可扩展训练逻辑

在特定的训练钩子处添加自定义功能，而无需修改LightningModule。内置回调包括：

- **ModelCheckpoint** - 保存最佳/最新模型
- **EarlyStopping** - 当指标平稳时停止
- **LearningRateMonitor** - 跟踪LR调度器变化
- **BatchSizeFinder** - 自动确定最佳批量大小

**详细文档：** 阅读`references/callbacks.md`获取内置回调和自定义回调创建。

### 5. Logging - 实验跟踪

与多个日志平台集成：

- TensorBoard（默认）
- Weights & Biases（WandbLogger）
- MLflow（MLFlowLogger）
- Neptune（NeptuneLogger）
- Comet（CometLogger）
- CSV（CSVLogger）

在任何LightningModule方法中使用`self.log("metric_name", value)`记录指标。

**详细文档：** 阅读`references/logging.md`获取日志器设置和配置。

### 6. Distributed Training - 扩展到多个设备

根据模型大小选择合适的策略：

- **DDP** - 适用于<500M参数的模型（ResNet、较小的Transformer）
- **FSDP** - 适用于500M+参数的模型（大型Transformer，推荐给Lightning用户）
- **DeepSpeed** - 适用于前沿特性和细粒度控制

配置：`Trainer(strategy="ddp", accelerator="gpu", devices=4)`

**详细文档：** 阅读`references/distributed_training.md`获取策略比较和配置。

### 7. 最佳实践

- 设备无关代码 - 使用`self.device`而不是`.cuda()`
- 超参数保存 - 在`__init__()`中使用`self.save_hyperparameters()`
- 指标记录 - 使用`self.log()`进行跨设备自动聚合
- 可重现性 - 使用`seed_everything()`和`Trainer(deterministic=True)`
- 调试 - 使用`Trainer(fast_dev_run=True)`测试1个批次

**详细文档：** 阅读`references/best_practices.md`获取常见模式和陷阱。

## 快速工作流

1. **定义模型：**
   ```python
   class MyModel(L.LightningModule):
       def __init__(self):
           super().__init__()
           self.save_hyperparameters()
           self.model = YourNetwork()

       def training_step(self, batch, batch_idx):
           x, y = batch
           loss = F.cross_entropy(self.model(x), y)
           self.log("train_loss", loss)
           return loss

       def configure_optimizers(self):
           return torch.optim.Adam(self.parameters())
   ```

2. **准备数据：**
   ```python
   # 选项1：直接使用DataLoaders
   train_loader = DataLoader(train_dataset, batch_size=32)

   # 选项2：LightningDataModule（推荐用于可重用性）
   dm = MyDataModule(batch_size=32)
   ```

3. **训练：**
   ```python
   trainer = L.Trainer(max_epochs=10, accelerator="gpu", devices=2)
   trainer.fit(model, train_loader)  # 或 trainer.fit(model, datamodule=dm)
   ```

## 资源

### scripts/

用于常见PyTorch Lightning模式的可执行Python模板：

- `template_lightning_module.py` - 完整的LightningModule样板代码
- `template_datamodule.py` - 完整的LightningDataModule样板代码
- `quick_trainer_setup.py` - 常见Trainer配置示例

### references/

每个PyTorch Lightning组件的详细文档：

- `lightning_module.md` - 综合LightningModule指南（方法、钩子、属性）
- `trainer.md` - Trainer配置和参数
- `data_module.md` - LightningDataModule模式和方法
- `callbacks.md` - 内置和自定义回调
- `logging.md` - 日志器集成和使用
- `distributed_training.md` - DDP、FSDP、DeepSpeed比较和设置
- `best_practices.md` - 常见模式、提示和陷阱