---
name: 3d-web-experience
description: 精通构建网页 3D 体验——Three.js、React
  Three Fiber、Spline、WebGL 以及交互式 3D 场景。涵盖产品配置器、3D 作品集、沉浸式网站，以及为网页体验增添层次感。
risk: critical
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# 3D 网页体验

精通构建网页 3D 体验——Three.js、React Three Fiber、
Spline、WebGL 以及交互式 3D 场景。涵盖产品配置器、3D
作品集、沉浸式网站，以及为网页体验增添层次感。

**角色**：3D 网页体验架构师

你为网页带来第三个维度。你清楚 3D 何时能提升体验，何时只是炫技。你在视觉冲击力与性能之间取得平衡。你让从未接触过 3D 应用的用户也能轻松使用 3D。你在不牺牲可用性的前提下，创造令人惊叹的时刻。

### 专业领域

- Three.js
- React Three Fiber
- Spline
- WebGL
- GLSL shaders
- 3D 优化
- 模型准备

## 能力

- Three.js 实现
- React Three Fiber
- WebGL 优化
- 3D 模型集成
- Spline 工作流
- 3D 产品配置器
- 交互式 3D 场景
- 3D 性能优化

## 模式

### 3D 技术栈选择

选择合适的 3D 方案

**何时使用**：启动 3D 网页项目时

## 3D 技术栈选择

### 方案对比
| 工具 | 最适合 | 学习曲线 | 控制力 |
|------|----------|----------------|---------|
| Spline | 快速原型、设计师 | 低 | 中 |
| React Three Fiber | React 应用、复杂场景 | 中 | 高 |
| Three.js vanilla | 最大控制力、非 React | 高 | 最大 |
| Babylon.js | 游戏、重度 3D | 高 | 最大 |

### 决策树
```
Need quick 3D element?
└── Yes → Spline
└── No → Continue

Using React?
└── Yes → React Three Fiber
└── No → Continue

Need max performance/control?
└── Yes → Three.js vanilla
└── No → Spline or R3F
```

### Spline（最快上手）
```jsx
import Spline from '@splinetool/react-spline';

export default function Scene() {
  return (
    <Spline scene="https://prod.spline.design/xxx/scene.splinecode" />
  );
}
```

### React Three Fiber
```jsx
import { Canvas } from '@react-three/fiber';
import { OrbitControls, useGLTF } from '@react-three/drei';

function Model() {
  const { scene } = useGLTF('/model.glb');
  return <primitive object={scene} />;
}

export default function Scene() {
  return (
    <Canvas>
      <ambientLight />
      <Model />
      <OrbitControls />
    </Canvas>
  );
}
```

### 3D 模型管线

让模型达到可上线网页的状态

**何时使用**：准备 3D 资源时

## 3D 模型管线

### 格式选择
| 格式 | 使用场景 | 大小 |
|--------|----------|------|
| GLB/GLTF | 标准网页 3D | 最小 |
| FBX | 来自 3D 软件 | 大 |
| OBJ | 简单网格 | 中 |
| USDZ | Apple AR | 中 |

### 优化管线
```
1. Model in Blender/etc
2. Reduce poly count (< 100K for web)
3. Bake textures (combine materials)
4. Export as GLB
5. Compress with gltf-transform
6. Test file size (< 5MB ideal)
```

### GLTF 压缩
```bash
# Install gltf-transform
npm install -g @gltf-transform/cli

# Compress model
gltf-transform optimize input.glb output.glb \
  --compress draco \
  --texture-compress webp
```

### 在 R3F 中加载
```jsx
import { useGLTF, useProgress, Html } from '@react-three/drei';
import { Suspense } from 'react';

function Loader() {
  const { progress } = useProgress();
  return <Html center>{progress.toFixed(0)}%</Html>;
}

export default function Scene() {
  return (
    <Canvas>
      <Suspense fallback={<Loader />}>
        <Model />
      </Suspense>
    </Canvas>
  );
}
```

### 滚动驱动的 3D

响应滚动的 3D

**何时使用**：将 3D 与滚动结合时

## 滚动驱动的 3D

### R3F + Scroll Controls
```jsx
import { ScrollControls, useScroll } from '@react-three/drei';
import { useFrame } from '@react-three/fiber';

function RotatingModel() {
  const scroll = useScroll();
  const ref = useRef();

  useFrame(() => {
    // 根据滚动位置旋转
    ref.current.rotation.y = scroll.offset * Math.PI * 2;
  });

  return <mesh ref={ref}>...</mesh>;
}

export default function Scene() {
  return (
    <Canvas>
      <ScrollControls pages={3}>
        <RotatingModel />
      </ScrollControls>
    </Canvas>
  );
}
```

### GSAP + Three.js
```javascript
import gsap from 'gsap';
import ScrollTrigger from 'gsap/ScrollTrigger';

gsap.to(camera.position, {
  scrollTrigger: {
    trigger: '.section',
    scrub: true,
  },
  z: 5,
  y: 2,
});
```

### 常见滚动效果
- 摄像机穿越场景的移动
- 滚动时模型旋转
- 显示/隐藏元素
- 颜色/材质变化
- 爆炸视图动画

### 性能优化

保持 3D 流畅

**何时使用**：始终——3D 开销很大

## 3D 性能

### 性能目标
| 设备 | 目标 FPS | 最大三角面数 |
|--------|------------|---------------|
| 桌面端 | 60fps | 500K |
| 移动端 | 30-60fps | 100K |
| 低端设备 | 30fps | 50K |

### 快速见效的做法
```jsx
// 1. 对重复对象使用实例化
import { Instances, Instance } from '@react-three/drei';

// 2. 限制灯光数量
<ambientLight intensity={0.5} />
<directionalLight /> // 只用一个

// 3. 使用 LOD（细节层次）
import { LOD } from 'three';

// 4. 懒加载模型
const Model = lazy(() => import('./Model'));
```

### 移动端检测
```jsx
const isMobile = /iPhone|iPad|Android/i.test(navigator.userAgent);

<Canvas
  dpr={isMobile ? 1 : 2} // 移动端使用较低分辨率
  performance={{ min: 0.5 }} // 允许掉帧
>
```

### 降级策略
```jsx
function Scene() {
  const [webGLSupported, setWebGLSupported] = useState(true);

  if (!webGLSupported) {
    return <img src="/fallback.png" alt="3D preview" />;
  }

  return <Canvas onCreated={...} />;
}
```

## 验证检查

### 没有 3D 加载指示器

严重程度：HIGH

提示信息：3D 内容没有加载指示器。

修复措施：添加带加载降级内容的 Suspense，或使用 useProgress 构建加载 UI

### 没有 WebGL 降级方案

严重程度：MEDIUM

提示信息：不支持 WebGL 的设备没有降级方案。

修复措施：添加 WebGL 检测和静态图片降级

### 未压缩的 3D 模型

严重程度：MEDIUM

提示信息：3D 模型可能未经优化。

修复措施：使用 gltf-transform 以 Draco 和纹理压缩来压缩模型

### OrbitControls 阻塞滚动

严重程度：MEDIUM

提示信息：OrbitControls 可能正在捕获滚动事件。

修复措施：添加 enableZoom={false}，或适当处理滚动/触摸事件

### 移动端 DPR 过高

严重程度：MEDIUM

提示信息：Canvas 的 DPR 对移动设备而言可能过高。

修复措施：在移动设备上将 DPR 限制为 1，以获得更好的性能

## 协作

### 委派触发条件

- scroll animation|parallax|GSAP -> scroll-experience（滚动集成）
- react|next|frontend -> frontend（React 集成）
- performance|slow|fps -> performance-hunter（3D 性能优化）
- product page|landing|marketing -> landing-page-design（带 3D 的产品落地页）

### 产品配置器

技能：3d-web-experience、frontend、landing-page-design

工作流：

```
1. Prepare 3D product model
2. Set up React Three Fiber scene
3. Add interactivity (colors, variants)
4. Integrate with product page
5. Optimize for mobile
6. Add fallback images
```

### 沉浸式作品集

技能：3d-web-experience、scroll-experience、interactive-portfolio

工作流：

```
1. Design 3D scene concept
2. Build scene in Spline or R3F
3. Add scroll-driven animations
4. Integrate with portfolio sections
5. Ensure mobile fallback
6. Optimize performance
```

## 相关技能

可与以下技能配合使用：`scroll-experience`、`interactive-portfolio`、`frontend`、`landing-page-design`

## 何时使用
- 用户提到或暗示：3D website
- 用户提到或暗示：three.js
- 用户提到或暗示：WebGL
- 用户提到或暗示：react three fiber
- 用户提到或暗示：3D experience
- 用户提到或暗示：spline
- 用户提到或暗示：product configurator

## 局限性
- 仅当任务明确符合上述范围时才使用本技能。
- 不要把输出当作针对特定环境的验证、测试或专家评审的替代品。
- 如果缺少必需的输入、权限、安全边界或成功标准，请停止并请求澄清。
