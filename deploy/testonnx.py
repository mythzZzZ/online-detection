from mmdeploy_runtime import Detector
import cv2
import os
class_name = ('pedestrian', 'people', 'bicycle', 'car', 'van', 'truck', 'tricycle', 'awning-tricycle', 'bus', 'motor')
palette=[(220, 20, 60), (119, 11, 32), (0, 0, 142), (0, 0, 230), (106, 0, 228),
         (0, 60, 100), (0, 80, 100), (0, 0, 70), (0, 0, 192), (250, 170, 30)]
def out_detection(input_image):
    img = cv2.imread(input_image)

    # create a detector
    detector = Detector(model_path='deploy',
                        device_name='cpu', device_id=0)
    # perform inference
    bboxes, labels, masks = detector(img)

    # visualize inference result
    indices = [i for i in range(len(bboxes))]
    for index, bbox, label_id in zip(indices, bboxes, labels):
        [left, top, right, bottom], score = bbox[0:4].astype(int), bbox[4]
        if score < 0.3:
            continue

        cv2.rectangle(img, (left, top), (right, bottom), palette[label_id])
        label_text = f'{class_name[label_id]}'
        # cv2.putText(img, label_text, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        # 计算标签文本的大小
        # 计算标签文本的大小
        (label_width, label_height), _ = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)

        # 计算标签放置的位置，位于检测边框的左上角
        text_x = left
        text_y = top

        # 绘制黑色矩形作为文本的背景
        cv2.rectangle(img, (text_x, text_y - label_height), (text_x + label_width, text_y), palette[label_id], -1)

        # 将白色文本放置在黑色矩形上方
        cv2.putText(img, label_text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
    basename = os.path.basename(input_image)
    print(basename)
    cv2.imwrite('media/output_obj_dect/'+basename, img)
    print('detection_success')
    return  ''.join(basename)