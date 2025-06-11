import torch, torch.nn as nn
from torchvision import models
import albumentations as AL
from albumentations.pytorch import ToTensorV2
from PIL import Image
import numpy as np
import os, cv2
import matplotlib.pyplot as plt
from ultralytics import YOLO


class EfficientNetDetector(nn.Module):
    def __init__(self, hidden_dim: int = 512):
        super().__init__()
        self.backbone = models.efficientnet_b4(weights=models.EfficientNet_B4_Weights.IMAGENET1K_V1)
        in_ch = self.backbone.classifier[1].in_features
        self.backbone.classifier = nn.Sequential(
            nn.Dropout(0.4, inplace=True),
            nn.Linear(in_ch, hidden_dim, bias=True),
            nn.ReLU(inplace=True),
            nn.Dropout(0.3, inplace=True),
            nn.Linear(hidden_dim, 2, bias=True)
        )
    def forward(self, x):
        return self.backbone(x)

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
if torch.backends.mps.is_available():  # M1/M2 + Metal 지원 여부
    DEVICE = "mps"

print(f"Using device: {DEVICE}")


test_tf = AL.Compose([
    AL.Resize(256, 256),
    AL.CenterCrop(224, 224),
    AL.Normalize(mean=(0.485,0.456,0.406), std=(0.229,0.224,0.225)),
    ToTensorV2(),
])
yolo_face = YOLO("yolov11m-face.pt")
yolo_face.to(DEVICE)
norm_tf = AL.Compose([
    AL.Normalize(mean=(0.485,0.456,0.406), std=(0.229,0.224,0.225)),
    ToTensorV2(),
])

model = EfficientNetDetector().to(DEVICE)
model.load_state_dict(torch.load("second.pth", map_location=DEVICE))
model.eval()

def crop_largest_face(pil_img: Image.Image) -> Image.Image:
    """YOLOv11로 얼굴 탐지 → 가장 넓은 박스 리턴, 없으면 중앙 224"""
    # PIL → numpy(BGR)
    img_bgr = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    res = yolo_face(img_bgr, imgsz=320, verbose=False)[0]           # 단일 이미지 추론
    if len(res.boxes):
        # 박스: (x1,y1,x2,y2,conf,cls)
        boxes = res.boxes.xyxy.cpu().numpy()                         # (N,4)
        areas = (boxes[:,2]-boxes[:,0])*(boxes[:,3]-boxes[:,1])
        x1,y1,x2,y2 = boxes[areas.argmax()]
        cx, cy = int((x1+x2)/2), int((y1+y2)/2)
        left  = max(cx-112, 0); upper = max(cy-112, 0)
        right = min(left+224, pil_img.width); left  = right-224
        lower = min(upper+224, pil_img.height); upper = lower-224
        return pil_img.crop((left,upper,right,lower))
    # 얼굴 없으면 중앙
    w,h = pil_img.size
    return pil_img.crop(((w-224)//2, (h-224)//2, (w+224)//2, (h+224)//2))

@torch.inference_mode()
def predict(path: str, th: float = 0.5, show: bool = True) -> float:
    img = Image.open(path).convert("RGB")

    img.thumbnail((450, 450), Image.BILINEAR)  # 긴 변 256px, 비율 유지

    crop = crop_largest_face(img)

    x = norm_tf(image=np.array(crop))["image"].unsqueeze(0).to(DEVICE)
    prob_fake = torch.softmax(model(x), dim=1)[0, 1].item()

    print(f"{os.path.basename(path):<20} Fake 확률: {prob_fake:.3%}  ->",
          "딥페이크 의심" if prob_fake > th else "정상")
    return prob_fake
