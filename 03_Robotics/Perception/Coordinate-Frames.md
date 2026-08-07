---
title: "机器人通用坐标系速查"
description: "机器人开发中常见坐标系的定义、转换关系与易错点——REP-103/105、OpenCV/OpenGL 相机系、URDF 关节系、数据集约定，以及典型桌面操作场景实例。"
tags: [robotics, coordinate-frames, ros, urdf, reference]
created: 2026-08-05
---

# 机器人通用坐标系速查

> 相关:[[03_Robotics/Perception/URDF-Rendering-Calibration|URDF 渲染几何标定方法]]、[[08_Experiments/URDF-Rendering-Calibration-Retro|标定复盘]]

## 1. 各体系坐标约定一览

| 体系 | x | y | z | 手性 | 备注 |
|---|---|---|---|---|---|
| **ROS REP-103**(机体) | 前 | 左 | 上 | 右手 | base_link 默认朝向 |
| **ROS REP-103**(世界) | 东 | 北 | 天(ENU) | 右手 | 室内机器人常自定义 |
| **典型桌面操作系** | 操作员右 | 操作员前方(桌面深处) | 上 | 右手 | = REP-103 绕 z 转 -90°，仅作示例 |
| **OpenCV 相机系** | 图像右 | 图像下 | 光轴向前 | 右手 | 视觉/标定(cv2)用 |
| **OpenGL/图形学相机系** | 图像右 | 图像上 | 光轴向后(-z 看出去) | 右手 | 渲染(pyrender)用 |
| **Unity** | 右 | 上 | 前 | **左手** | 跨引擎注意 |
| **Blender** | 右 | 后 | 上 | 右手 | 导入导出网格注意 |
| **Isaac Sim/USD** | 右 | 后 | 上(Z-up 层) | 右手 | 部分资产 Y-up |

## 2. ROS 标准坐标树(REP-105)

```
earth → map → odom → base_link → sensor_frame / arm joints → tool
```

| 帧 | 含义 | 特性 |
|---|---|---|
| `earth` | ECEF,多地图场景才用 | rarely used |
| `map` | 全局不动系(如建图原点) | 长期不漂移,允许跳变(重定位) |
| `odom` | 里程计原点 | 连续但长期漂移 |
| `base_link` | 机器人本体 | REP-103:x 前 y 左 z 上 |
| `tool0` / `flange` / `tcp` | 机械臂末端:法兰中心 / 工具坐标 | tool0 到 tcp 由工具标定给出 |

**TF 规则**:父子帧都是 4×4 刚体变换;`T_parent_child` 表示 child 系原点在 parent 系中的位姿;点坐标左乘下溯:`p_parent = T_parent_child @ p_child`。

## 3. URDF 约定

- 全部坐标系**右手系**,单位:米、弧度
- `base_link` 由 URDF 作者自定,通常 z 沿第一关节轴(例如某双臂平台 base +z = joint1 轴,竖直向上)
- 关节原点 `origin xyz/rpy`:该关节系相对**父连杆**系的位姿(零位时)
- 关节旋转绕自身 `axis`,正方向 = 右手定则
- 常见坑:
  - **数据零位 ≠ URDF 零位**(编码器零点/安装方式决定,需逐臂标定)
  - **控制器符号 ≠ URDF 符号**(电机安装方向,应逐关节 jog 验证,不要默认)
  - 可视化(mesh visual)与运动学(origin)是两套 origin,别混用

## 4. 相机系:OpenCV vs OpenGL(视觉-渲染交界最易错)

```
OpenCV:  x→右  y→下  z→光轴向前    (cv2.projectPoints, 标定)
OpenGL:  x→右  y→上  z→光轴向后    (pyrender, OpenGL)
转换:    R_gl = diag(1,-1,-1) @ R_cv  (绕 x 翻 180°)
```

- 投影公式(OpenCV):`u = fx·X/Z + cx, v = fy·Y/Z + cy`,深度 Z>0 在相机前方
- 畸变(Brown):先归一化再 `r²` 多项式,与分辨率无关;广角必须建模 k1/k2
- pyrender 相机 pose 是 OpenGL 系,给 OpenCV 外参必须乘 `diag(1,-1,-1)`

## 5. 旋转表示法速查

| 表示 | 约定 | 坑 |
|---|---|---|
| 欧拉角 | **固定轴 XYZ** ≡ 内旋 ZYX(`R = Rz(rz)Ry(ry)Rx(rx)`);ROS/URDF rpy 即此 | "内旋/外旋、XYZ/ZYX"说法混乱,写成矩阵乘积最保险 |
| 四元数 | ROS/Eigen:**(x,y,z,w)**;scipy:**(x,y,z,w)**;部分库/文档:**(w,x,y,z)** | 顺序!读接口文档,别猜 |
| 旋转向量 | `cv2.Rodrigues`,轴角×模长 | 与欧拉角不是一回事 |
| 提取欧拉角(R=RzRyRx) | `ry=asin(-R[2,0]); rx=atan2(R[2,1],R[2,2]); rz=atan2(R[1,0],R[0,0])` | 万向锁 ry=±90° 时 rx/rz 退化 |

## 6. 位姿组合与求逆(每天在用)

```
T_AB : B 系在 A 系中的位姿(A←B)
点变换:  p_A = T_AB @ p_B
链式:    T_AC = T_AB @ T_BC
求逆:    T_BA = [R^T | -R^T t]
位姿"插值/微调":  T' = ΔT(在 A 系) @ T  或  T @ ΔT(在 B 系)
```

**最常犯的错误**:把"相机在世界系的位置 pos"直接当成 `T_world_cam` 的平移分量——正确的是 `t = -R @ pos`。

## 7. 数据集/算法侧约定

| 来源 | 约定 |
|---|---|
| **LeRobot** | `observation.state` 关节弧度,顺序见 `meta/info.json`;视频帧与时间戳 30fps 严格对齐;`action[t]≈state[t+1]`(可移位补齐缺失 state) |
| **SAM/SAM3** | 输入 RGB uint8,mask 为 (H,W) bool,xy 顺序=列行 |
| **cv2 vs PIL** | cv2 默认 BGR、PIL/imageio 默认 RGB——跨库传图先确认通道序 |
| **numpy 图像** | (H,W,C),索引 [y,x];与"点坐标 (x,y)"相反,投影后取像素注意转置 |

## 8. 典型坐标链(示例)

```
parquet q (弧度, 例如 14 维: 左6+左爪 | 右6+右爪)
  └─ sign/offset 修正 → URDF 关节角
      └─ FK → 连杆在各自 base 系位姿
          └─ T_world_base(基座实测: 例如 ±0.3m, θ0≈π/2, 微调 y/z/yaw)
              └─ T_cam_world(相机外参标定)
                  └─ 针孔 fx + 畸变 k1 → 像素
```

每环都可能藏一个符号/偏移错误;静止帧对齐只能验证几何链,**运动帧才能验证关节约定**,时序视频才能验证时间同步——三层验收缺一不可。
