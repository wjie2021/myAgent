# 哼唱转旋律

把哼唱的旋律转换成乐谱，然后播放出来。

## 核心思路

不依赖专业音乐 AI 模型，用通用工具组合实现：

```
哼唱录音 → 音高检测 → 生成 ABC 记谱法 → 在线播放 → AI 扩充
```

## 技术方案

### 方案一：网页版（单文件，零依赖）

直接浏览器打开 `index.html`，不需要安装任何东西。

| 环节 | 技术 | 说明 |
|------|------|------|
| 录音 | MediaRecorder API | 浏览器原生，按按钮开始/停止 |
| 音高检测 | Autocorrelation 算法 | 自相关算法检测基频，纯 JS 实现 |
| Hz → 音符 | 公式计算 | `MIDI = 12 * log2(freq/440) + 69` |
| 生成 ABC | 字符串拼接 | 音符序列 + 节拍信息 → ABC 文本 |
| 播放 | abcjs 库 | CDN 引入，粘贴 ABC 直接听 |

### 方案二：Python 版（更灵活）

适合后续扩展，比如接入 AI 生成、批量处理等。

| 环节 | 库 | 说明 |
|------|-----|------|
| 录音 | `sounddevice` | 按回车开始/停止 |
| 音高检测 | `librosa.pyin()` | pYIN 算法，精度更高 |
| Hz → 音符 | `numpy` + 公式 | 同上 |
| 生成 ABC | 字符串拼接 | 同上 |
| 播放 | `abcjs` (浏览器) | 生成 HTML 文件，自动打开 |

## 关键公式

```python
# 频率转 MIDI 音符号
MIDI = 12 * log2(freq / 440) + 69

# MIDI 音符号转音名
note_names = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
note = note_names[MIDI % 12]
octave = (MIDI // 12) - 1

# BPM 转每拍时长
beat_duration = 60 / bpm  # 秒
```

## ABC 记谱法速查

```
X:1          # 编号
T:标题       # 标题
M:4/4        # 拍号
L:1/4        # 默认音符时值
K:C          # 调号

C D E F | G A B c |   # 大写=中音，小写=高音
C, D, E, |              # 逗号=低八度
c' d' e' |              # 撇号=高八度
C2 D3 |                  # 数字=时值倍数
```

## 在线播放工具

- [abcjs 在线编辑器](https://www.abcjs.net/abcjs-editor.html) — 左边写 ABC，右边实时播放
- [abcnotation.com](https://abcnotation.com/) — ABC 记谱法官方资源

## 当前状态

- [x] 网页版 v0.1（基础录音 + 音高检测 + ABC 生成 + 播放）
- [ ] Python 版
- [ ] AI 扩充功能

## 使用方法

### 网页版

直接浏览器打开 `index.html`，允许麦克风权限后即可使用。

### 让 AI 扩充旋律

复制生成的 ABC 记谱法，发给 Claude/GPT，说：

> "基于这段旋律，加上和弦伴奏，让它更丰富"
