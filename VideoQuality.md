# 视频质量检测

* 清晰度异常
* 雪花
* 波纹
* 亮度异常
* 偏色
* 信号丢失

## 1. 清晰度异常检测
由于前端摄像机视频中聚焦不当，异物遮挡等原因，所引起的画面视野图像模糊的现象。<br/>
算法解决原理：<br/>
把彩色图像转化为灰度图像，对灰度图像的做边缘检测，采用sobel算子做处理，
计算边缘的平均值，小于一定阈值则认为是清晰度异常。
sobel算子对灰度渐变和噪声较多的图像处理效果比较好，对边缘定位比较准确。<br/>
[图像梯度计算&边缘检测](https://www.cnblogs.com/wj-1314/p/9800272.html)

## 2. 雪花检测
方法:<br/>
1. 准备0°，45°，90°，135°4个方向的卷积模板。
2. 用图像先和四个模板做卷积，用四个卷积绝对值最小值Min来检测噪声点。
3. 求灰度图gray与其中值滤波图median。
4. 判断噪声点：fabs(median-gray)>10 && min>0.1。
5. 噪声点占整幅图像的比较即为雪花噪声率。

## 3. 波纹检测
方法：<br/>
1. 提取彩色图像的色度分量。
2. 对色度分量求DFT频谱图。
3. 计算频谱图的异常亮点数，若大于A(0.004)则认为发生条纹检测。

## 4. 亮度异常检测
计算图片在灰度图上的均值和方差，当存在亮度异常时，
均值会偏离均值点（可以假设为128），方差也会偏小；通过计算灰度图的均值和方差，
就可评估图像是否存在过曝光或曝光不足。
- RGB 图像转为灰度图像

- 计算灰度图像偏离均值点(128)的均值 $d_a=\frac{\sum\limits_{i=0}^{N-1}(x_i-128)}{N}$ 其中N是灰度图像素点的个数, $N=width*height$, $x_i$为灰度图各个像素点的值.

- $D=|d_a|$

- 偏离128的平均偏差 $M_a=\frac{\sum\limits_{i=0}^{255}|(i-128)-d_a|*Hist[i]}{N}, M=|m_a|$, Hist为灰度图的直方图.

- 亮度系数 $K=\frac{D}{M}$

- $$
  \begin{cases}
  K \geqslant 1, & \text{亮度异常} \Rightarrow \begin{cases} d_a > 0, & \text{过亮} \\ d_a \leqslant 0, & \text{过暗} \end{cases} \\
  K < 1, & \text{亮度正常}
  \end{cases}
  $$

## 5. 偏色检测
将RGB图像转变到CIE Lab空间，其中L表示图像亮度，a表示图像红/绿分量，b表示图像黄/蓝分量。通常存在色偏的图像，在a和b分量上的均值会偏离原点很远，方差也会偏小；
通过计算图像在a和b分量上的均值和方差，就可评估图像是否存在色偏。

[算法](https://blog.csdn.net/fightingforcv/article/details/52724848)

计算偏色因子, 大于1.5,认为偏色; 小于1.5,认为正常.

## 6. 信号丢失(黑屏)检测

- 将彩色图像二值化
- 求最大连通区域, 求得最大连同区域的面积
- 将该面积除以整服图像的面积,求得信号丢失率
- 设定阈值(0.8),丢失率大于阈值,判定为信号丢失;小于阈值判定为正常



文件树:

```
├── estimate.py
├── managers.py
├── noise.py
├── quality.py
├── VideoQuality.md
└── video_src
    └── 62-清晰度异常.avi
```



运行:

```
python quality.py --input={path to input video} --output={path to output} --method={method} --thred{thred}
--method=0 模糊检测
--method=1 波纹检测
--method=2 亮度异常检测
--method=3 偏色检测
--method=4 信号丢失检测
--method=5 雪花检测

--thred={float} 检测阈值
推荐值:
模糊检测: 1500 
波纹检测: 0.004 
亮度异常检测: 不设置thred
偏色检测: 1.5  
信号丢失检测: 0.8 
雪花检测:0.04
```

命令行运行:

```
python quality.py --input='./video_src/62-清晰度异常.avi' --output='./video_src/62output.avi' --method=0 --thred=1500
```

运行结束,按<esc>键关闭窗口,退出.