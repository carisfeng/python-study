from paddleocr import PaddleOCR, draw_ocr
from PIL import Image
# Paddleocr supports Chinese, English, French, German, Korean and Japanese.
# You can set the parameter `lang` as `ch`, `en`, `french`, `german`, `korean`, `japan`
# to switch the language model in order.
ocr = PaddleOCR(use_angle_cls=True, lang='ch')  # need to run only once to download and load model into memory
img_path = '0000520701.jpg'
result = ocr.ocr(img_path, cls=True)
print(result)
for line in result:
    print(line)
image = Image.open(img_path).convert('RGB')
boxes = [line[0] for line in result]
txts = [line[1][0] for line in result]
scores = [line[1][1] for line in result]
im_show = draw_ocr(image, boxes, txts, scores)
im_show = Image.fromarray(im_show)
im_show.save('result.jpg')

# 在命令行输入以下命令，创建名为paddle_env的环境
# 此处为加速下载，使用清华源
conda create --name paddle_env python=3.10 --channel https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/

Preparing transaction: done                                                                                         
Verifying transaction: / WARNING conda.core.path_actions:verify(1094): Unable to create environments file. Path not writable.                                                                                                           
  environment location: /Users/caris/.conda/environments.txt                                                        
                                                                                                                    
done                                                                                                                
Executing transaction: | WARNING conda.core.envs_manager:register_env(49): Unable to register environment. Path not writable or missing.
  environment location: /opt/homebrew/anaconda3/envs/paddle_env
  registry file: /Users/caris/.conda/environments.txt
done




# To activate this environment, use
#
#     $ conda activate paddle_env
#
# To deactivate an active environment, use
#
#     $ conda deactivate

