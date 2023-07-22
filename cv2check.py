# 1、灰度化读取文件
filepath = '/tmp/rotated.png'
img = cv2.imread(filepath, 0)
if img is None:
    LOG.error('image not exists!')
    exit()

# 2、图像延扩
h, w = img.shape[:2]
new_h = cv2.getOptimalDFTSize(h)  # 傅里叶最优尺寸
new_w = cv2.getOptimalDFTSize(w)
right = new_w - w
bottom = new_h - h
# 边界扩充 cv2.copyMakeBorder(src, top, bottom, left, right, borderType, dst=None)
#   BORDER_CONSTANT    常量，增加的变量通通为 value
#   BORDER_REFLICATE   用边界的颜色填充
#   BORDER_REFLECT     镜像
#   BORDER_REFLECT_101 倒映
#   BORDER_WRAP        没有规律
nimg = cv2.copyMakeBorder(img, 0, bottom, 0, right, borderType=cv2.BORDER_CONSTANT, value=0)
cv2.imshow('new image', nimg)

# 3、傅里叶变换，获到频域图像
f = np.fft.fft2(nimg)
fshift = np.fft.fftshift(f)
magnitude = np.log(np.abs(fshift))
LOG.info(magnitude)
# 二值化
magnitude_uint = magnitude.astype(np.uint8)
ret, thresh = cv2.threshold(magnitude_uint, 11, 255, cv2.THRESH_BINARY)
LOG.info(ret)
cv2.imshow('thresh', thresh)
LOG.info(thresh.dtype)

# 4、霍夫直线变换
lines = cv2.HoughLinesP(thresh, 2, np.pi/180, 30, minLineLength=40, maxLineGap=100)
LOG.info('line number: %d', len(lines))
# 创建一个新图像，标注直线
lineimg = np.ones(nimg.shape, dtype=np.uint8)
lineimg = lineimg * 255
for index, line in enumerate(lines):
    LOG.info('draw line#%d: %s', index, line)
    x1, y1, x2, y2 = line[0]
    cv2.line(lineimg, (x1, y1), (x2, y2), (0, 255, 0), 2)
cv2.imshow('line image', lineimg)

# 5、计算倾斜角度
piThresh = np.pi / 180
pi2 = np.pi / 2
angles = []
for line in lines:
    LOG.info('line#%d: %s <===============', index, line)
    x1, y1, x2, y2 = line[0]
    if x2 - x1 == 0:
        LOG.debug('skip 1')
        continue
    theta = (y2 - y1) / (x2 - x1)
    LOG.debug('theta: %r', theta)
    if abs(theta) < piThresh or abs(theta - pi2) < piThresh:
        LOG.debug('skip 2: %r', theta)
        continue
    angle = math.atan(theta)
    LOG.info('angle 1: %r', angle)
    angle = angle * (180 / np.pi)
    LOG.info('angle 2: %r', angle)
    angle = (angle - 90)/(w/h)
    LOG.info('angle 3: %r', angle)
    angles.append(angle)

if not angles:
    LOG.info('图片挺正的了，别折腾！')
else:
    # from numpy.lib.function_base import average
    # angle = average(angles)
    LOG.info('  方差: %r', np.array(angles).var())
    LOG.info('标准差: %r', np.array(angles).std())
    # angle = np.mean(angles)
    import statistics
    # LOG.debug(statistics.multimode(angles))
    # angle = statistics.mode(angles)
    # statistics.StatisticsError: geometric mean requires a non-empty dataset  containing positive numbers
    # statistics.StatisticsError: harmonic mean does not support negative values
    angle = statistics.median(angles)
    if 180 > angle > 90:
        angle = 180 - angle
    elif -180 < angle < -90:
        angle = 180 + angle
    LOG.info('==> %r, %r', angles, angle)

    # 6、旋转
    center = (w//2, h//2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    LOG.debug('=========== RotationMatrix2D ===========')
    for i in M:
        LOG.debug(i)
    LOG.debug('^======================================^')
    rotated = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    cv2.imshow('rotated', rotated)

cv2.waitKey(0)
cv2.destroyAllWindows()