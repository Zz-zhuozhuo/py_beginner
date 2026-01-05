import torch
import cv2

# 加载YOLOv5模型（预训练于COCO 80类，意思是可以检测80种常见物体，已经训练好）
# 如果需要检测其他类别，可以加载自定义训练的模型
# 这里使用的是YOLOv5s（small）版本，速度快但精度稍低
# 如果需要更高精度，可以使用YOLOv5m（medium）或YOLOv5l（large）
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# 打开摄像头
cap = cv2.VideoCapture(0)
print("📷 摄像头打开，按 'q' 退出")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 推理（frame是BGR，自动转换）
    results = model(frame)

    # 画框 & 标签（可选 render）
    annotated_frame = results.render()[0]

    # 显示画面
    cv2.imshow('YOLOv5 目标检测', annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
