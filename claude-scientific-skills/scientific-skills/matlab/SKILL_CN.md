---
name: matlab
description: MATLAB 和 GNU Octave 数值计算，用于矩阵运算、数据分析、可视化和科学计算。当编写 MATLAB/Octave 脚本进行线性代数、信号处理、图像处理、微分方程、优化、统计或创建科学可视化时使用。也适用于用户需要 MATLAB 语法、函数帮助或希望在 MATLAB 和 Python 代码之间转换的情况。脚本可以用 MATLAB 或开源 GNU Octave 解释器执行。
license: For MATLAB (https://www.mathworks.com/pricing-licensing.html) and for Octave (GNU General Public License version 3)
compatibility: Requires either MATLAB or Octave to be installed for testing, but not required for just generating scripts.
metadata:
    skill-author: K-Dense Inc.
---

# MATLAB/Octave 科学计算

MATLAB 是一个为矩阵运算和科学计算优化的数值计算环境。GNU Octave 是一个免费的开源替代品，与 MATLAB 高度兼容。

## 快速开始

**运行 MATLAB 脚本：**
```bash
# MATLAB (商业版)
matlab -nodisplay -nosplash -r "run('script.m'); exit;"

# GNU Octave (免费，开源)
octave script.m
```

**安装 GNU Octave：**
```bash
# macOS
brew install octave

# Ubuntu/Debian
sudo apt install octave

# Windows - 从 https://octave.org/download 下载
```

## 核心能力

### 1. 矩阵运算

MATLAB 基本操作矩阵和数组：

```matlab
% 创建矩阵
A = [1 2 3; 4 5 6; 7 8 9];  % 3x3 矩阵
v = 1:10;                     % 行向量 1 到 10
v = linspace(0, 1, 100);      % 从 0 到 1 的 100 个点

% 特殊矩阵
I = eye(3);          % 单位矩阵
Z = zeros(3, 4);     % 3x4 零矩阵
O = ones(2, 3);      % 2x3 全 1 矩阵
R = rand(3, 3);      % 均匀分布随机矩阵
N = randn(3, 3);     % 正态分布随机矩阵

% 矩阵运算
B = A';              % 转置
C = A * B;           % 矩阵乘法
D = A .* B;          % 元素级乘法
E = A \ b;           % 解线性系统 Ax = b
F = inv(A);          % 矩阵求逆
```

完整的矩阵运算，请参见 [references/matrices-arrays.md](references/matrices-arrays.md)。

### 2. 线性代数

```matlab
% 特征值和特征向量
[V, D] = eig(A);     % V: 特征向量, D: 对角特征值

% 奇异值分解
[U, S, V] = svd(A);

% 矩阵分解
[L, U] = lu(A);      % LU 分解
[Q, R] = qr(A);      % QR 分解
R = chol(A);         % Cholesky（对称正定）

% 解线性系统
x = A \ b;           % 首选方法
x = linsolve(A, b);  % 带选项
x = inv(A) * b;      % 效率较低
```

全面的线性代数，请参见 [references/mathematics.md](references/mathematics.md)。

### 3. 绘图和可视化

```matlab
% 2D 图
x = 0:0.1:2*pi;
y = sin(x);
plot(x, y, 'b-', 'LineWidth', 2);
xlabel('x'); ylabel('sin(x)');
title('正弦波');
grid on;

% 多图
hold on;
plot(x, cos(x), 'r--');
legend('sin', 'cos');
hold off;

% 3D 曲面
[X, Y] = meshgrid(-2:0.1:2, -2:0.1:2);
Z = X.^2 + Y.^2;
surf(X, Y, Z);
colorbar;

% 保存图形
saveas(gcf, 'plot.png');
print('-dpdf', 'plot.pdf');
```

完整的可视化指南，请参见 [references/graphics-visualization.md](references/graphics-visualization.md)。

### 4. 数据导入/导出

```matlab
% 读取表格数据
T = readtable('data.csv');
M = readmatrix('data.csv');

% 写入数据
writetable(T, 'output.csv');
writematrix(M, 'output.csv');

% MAT 文件（MATLAB 原生）
save('data.mat', 'A', 'B', 'C');  % 保存变量
load('data.mat');                   % 加载所有
S = load('data.mat', 'A');         % 加载特定变量

% 图像
img = imread('image.png');
imwrite(img, 'output.jpg');
```

完整的 I/O 指南，请参见 [references/data-import-export.md](references/data-import-export.md)。

### 5. 控制流和函数

```matlab
% 条件语句
if x > 0
    disp('positive');
elseif x < 0
    disp('negative');
else
    disp('zero');
end

% 循环
for i = 1:10
    disp(i);
end

while x > 0
    x = x - 1;
end

% 函数（在单独的 .m 文件或同一文件中）
function y = myfunction(x, n)
    y = x.^n;
end

% 匿名函数
f = @(x) x.^2 + 2*x + 1;
result = f(5);  % 36
```

完整的编程指南，请参见 [references/programming.md](references/programming.md)。

### 6. 统计和数据分析

```matlab
% 描述性统计
m = mean(data);
s = std(data);
v = var(data);
med = median(data);
[minVal, minIdx] = min(data);
[maxVal, maxIdx] = max(data);

% 相关性
R = corrcoef(X, Y);
C = cov(X, Y);

% 线性回归
p = polyfit(x, y, 1);  % 线性拟合
y_fit = polyval(p, x);

% 移动统计
y_smooth = movmean(y, 5);  % 5点移动平均
```

统计参考，请参见 [references/mathematics.md](references/mathematics.md)。

### 7. 微分方程

```matlab
% ODE 求解
% dy/dt = -2y, y(0) = 1
f = @(t, y) -2*y;
[t, y] = ode45(f, [0 5], 1);
plot(t, y);

% 高阶：y'' + 2y' + y = 0
% 转换为系统：y1' = y2, y2' = -2*y2 - y1
f = @(t, y) [y(2); -2*y(2) - y(1)];
[t, y] = ode45(f, [0 10], [1; 0]);
```

ODE 求解器指南，请参见 [references/mathematics.md](references/mathematics.md)。

### 8. 信号处理

```matlab
% FFT
Y = fft(signal);
f = (0:length(Y)-1) * fs / length(Y);
plot(f, abs(Y));

% 滤波
b = fir1(50, 0.3);           % FIR 滤波器设计
y_filtered = filter(b, 1, signal);

% 卷积
y = conv(x, h, 'same');
```

信号处理，请参见 [references/mathematics.md](references/mathematics.md)。

## 常见模式

### 模式 1：数据分析管道

```matlab
% 加载数据
data = readtable('experiment.csv');

% 清理数据
data = rmmissing(data);  % 移除缺失值

% 分析
grouped = groupsummary(data, 'Category', 'mean', 'Value');

% 可视化
figure;
bar(grouped.Category, grouped.mean_Value);
xlabel('Category'); ylabel('Mean Value');
title('Results by Category');

% 保存
writetable(grouped, 'results.csv');
saveas(gcf, 'results.png');
```

### 模式 2：数值模拟

```matlab
% 参数
L = 1; N = 100; T = 10; dt = 0.01;
x = linspace(0, L, N);
dx = x(2) - x(1);

% 初始条件
u = sin(pi * x);

% 时间步进（热方程）
for t = 0:dt:T
    u_new = u;
    for i = 2:N-1
        u_new(i) = u(i) + dt/(dx^2) * (u(i+1) - 2*u(i) + u(i-1));
    end
    u = u_new;
end

plot(x, u);
```

### 模式 3：批处理

```matlab
% 处理多个文件
files = dir('data/*.csv');
results = cell(length(files), 1);

for i = 1:length(files)
    data = readtable(fullfile(files(i).folder, files(i).name));
    results{i} = analyze(data);  % 自定义分析函数
end

% 合并结果
all_results = vertcat(results{:});
```

## 参考文件

- **[matrices-arrays.md](references/matrices-arrays.md)** - 矩阵创建、索引、操作和运算
- **[mathematics.md](references/mathematics.md)** - 线性代数、微积分、ODE、优化、统计
- **[graphics-visualization.md](references/graphics-visualization.md)** - 2D/3D 绘图、自定义、导出
- **[data-import-export.md](references/data-import-export.md)** - 文件 I/O、表格、数据格式
- **[programming.md](references/programming.md)** - 函数、脚本、控制流、OOP
- **[python-integration.md](references/python-integration.md)** - 从 MATLAB 调用 Python 及反之
- **[octave-compatibility.md](references/octave-compatibility.md)** - MATLAB 和 GNU Octave 之间的差异
- **[executing-scripts.md](references/executing-scripts.md)** - 执行生成的脚本和测试

## GNU Octave 兼容性

GNU Octave 与 MATLAB 高度兼容。大多数脚本无需修改即可工作。主要差异：

- 使用 `#` 或 `%` 进行注释（MATLAB 仅使用 `%`）
- Octave 允许 `++`、`--`、`+=` 运算符
- 某些工具箱函数在 Octave 中不可用
- 使用 `pkg load` 加载 Octave 包

完整的兼容性指南，请参见 [references/octave-compatibility.md](references/octave-compatibility.md)。

## 使用示例

### 矩阵运算

```matlab
% 创建矩阵
A = [1 2 3; 4 5 6; 7 8 9];
B = [9 8 7; 6 5 4; 3 2 1];

% 矩阵运算
C = A + B;      % 矩阵加法
D = A * B;      % 矩阵乘法
E = A';         % 矩阵转置
F = inv(A);     % 矩阵求逆

% 显示结果
disp('A + B =');
disp(C);
disp('A * B =');
disp(D);
```

### 傅里叶变换

```matlab
% 生成信号
fs = 1000;              % 采样频率
t = 0:1/fs:1-1/fs;     % 时间向量
f1 = 50;               % 频率1
f2 = 120;              % 频率2
x = sin(2*pi*f1*t) + sin(2*pi*f2*t);

% 计算FFT
N = length(x);
X = fft(x);
P2 = abs(X/N);
P1 = P2(1:N/2+1);
P1(2:end-1) = 2*P1(2:end-1);
f = fs*(0:(N/2))/N;

% 绘制频谱
figure;
plot(f, P1);
title('单边幅度谱');
xlabel('频率 (Hz)');
ylabel('幅度');
grid on;
```

### 图像处理

```matlab
% 读取图像
img = imread('peppers.png');

% 转换为灰度图像
gray_img = rgb2gray(img);

% 高斯滤波
filtered_img = imgaussfilt(gray_img, 2);

% 边缘检测
edge_img = edge(filtered_img, 'Canny');

% 显示图像
figure;
subplot(2, 2, 1);
imshow(img);
title('原始图像');

subplot(2, 2, 2);
imshow(gray_img);
title('灰度图像');

subplot(2, 2, 3);
imshow(filtered_img);
title('滤波后图像');

subplot(2, 2, 4);
imshow(edge_img);
title('边缘检测');
```

### 控制系统

```matlab
% 定义传递函数
num = [1];
den = [1 2 1];
sys = tf(num, den);

% 绘制阶跃响应
figure;
step(sys);
title('阶跃响应');
grid on;

% 绘制伯德图
figure;
bode(sys);
title('伯德图');
grid on;

% 绘制根轨迹
figure;
rlocus(sys);
title('根轨迹');
grid on;
```

### 机器学习

```matlab
% 加载数据
load fisheriris

% 提取特征和标签
X = meas;
Y = species;

% 分割数据
cv = cvpartition(Y, 'HoldOut', 0.3);
idx = cv.test;

% 训练模型
X_train = X(~idx, :);
Y_train = Y(~idx, :);
X_test = X(idx, :);
Y_test = Y(idx, :);

% 训练SVM分类器
SVMModel = fitcsvm(X_train, Y_train);

% 预测
Y_pred = predict(SVMModel, X_test);

% 计算准确率
accuracy = sum(strcmp(Y_pred, Y_test)) / length(Y_test);
disp(['准确率: ', num2str(accuracy)]);
```

### 深度学习

```matlab
% 加载数据
[XTrain, YTrain] = digitTrain4DArrayData;

% 定义网络
layers = [
    imageInputLayer([28 28 1], 'Name', 'input')
    convolution2dLayer(3, 8, 'Padding', 'same', 'Name', 'conv1')
    batchNormalizationLayer('Name', 'bn1')
    reluLayer('Name', 'relu1')
    maxPooling2dLayer(2, 'Stride', 2, 'Name', 'maxpool1')
    convolution2dLayer(3, 16, 'Padding', 'same', 'Name', 'conv2')
    batchNormalizationLayer('Name', 'bn2')
    reluLayer('Name', 'relu2')
    maxPooling2dLayer(2, 'Stride', 2, 'Name', 'maxpool2')
    fullyConnectedLayer(10, 'Name', 'fc')
    softmaxLayer('Name', 'softmax')
    classificationLayer('Name', 'output')
];

% 训练选项
options = trainingOptions('adam', ...
    'MaxEpochs', 10, ...
    'MiniBatchSize', 128, ...
    'InitialLearnRate', 0.01, ...
    'Plots', 'training-progress');

% 训练网络
net = trainNetwork(XTrain, YTrain, layers, options);

% 测试网络
[XTest, YTest] = digitTest4DArrayData;
YPred = classify(net, XTest);
accuracy = mean(YPred == YTest);
disp(['准确率: ', num2str(accuracy)]);
```

## 最佳实践

1. **向量化操作** - 尽可能避免循环：
   ```matlab
   % 慢
   for i = 1:1000
       y(i) = sin(x(i));
   end

   % 快
   y = sin(x);
   ```

2. **预分配数组** - 避免在循环中增长数组：
   ```matlab
   % 慢
   for i = 1:1000
       y(i) = i^2;
   end

   % 快
   y = zeros(1, 1000);
   for i = 1:1000
       y(i) = i^2;
   end
   ```

3. **使用适当的数据类型** - 混合数据使用表格，数值数据使用矩阵：
   ```matlab
   % 数值数据
   M = readmatrix('numbers.csv');

   % 带表头的混合数据
   T = readtable('mixed.csv');
   ```

4. **注释和文档** - 使用函数帮助：
   ```matlab
   function y = myfunction(x)
   %MYFUNCTION 简短描述
   %   Y = MYFUNCTION(X) 详细描述
   %
   %   示例:
   %       y = myfunction(5);
       y = x.^2;
   end
   ```

## 其他资源

- MATLAB 文档：https://www.mathworks.com/help/matlab/
- GNU Octave 手册：https://docs.octave.org/latest/
- MATLAB Onramp（免费课程）：https://www.mathworks.com/learn/tutorials/matlab-onramp.html
- File Exchange：https://www.mathworks.com/matlabcentral/fileexchange/
