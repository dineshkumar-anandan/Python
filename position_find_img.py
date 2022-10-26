import cv2
import pytesseract
from pytesseract import Output
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

img_path = "/home/dineshkumar.anandan@zucisystems.com/Workspace/position_identification/data/ESI_CC_Form_1_Fax_urgent_0.jpg"

value = ["1417948720"]


def extract_words(img, ocr_engine='pytesseract'):
    if ocr_engine == 'pytesseract':
        data = pytesseract.image_to_data(img, output_type=Output.DICT)
        n_boxes = len(data['text'])
        words = [
            {
                'text': data['text'][i],
                'left': data['left'][i],
                'top': data['top'][i],
                'right': data['left'][i] + data['width'][i],
                'bottom': data['top'][i] + data['height'][i]
            }
            for i in range(n_boxes) if data['text'][i]
        ]
        return words


tesseract_output = extract_words(img_path)

image = cv2.imread(img_path)

for value in value:

    values_list = value.split()

    output = []
    dup_list = []

    stat_left_value = []

    for values in values_list:

        for text in tesseract_output:

            if values.lower() in text['text'].lower():
                output.append(text)

    for i in range(len(output)):
        dup_list.append(output[i]['top'])

    dup = {x for x in dup_list if dup_list.count(x) > 1}

    dup_value = list(dup)[0]

    text_all = []
    out = []
    for i in range(len(output)):
        if output[i]['top'] == dup_value:
            stat_left_value.append(output[i]['left'])
            if output[i]['left'] >= stat_left_value[0]:
                print(output[i])
                out.append(output[i])
                text_all.append(output[i]['text'])

    image = cv2.rectangle(image, (out[0]['left'], out[0]['bottom']), (out[-1]['right'], out[-1]['top']), (255, 0, 0), 2)

    cv2.imwrite("/home/dineshkumar.anandan@zucisystems.com/Workspace/position_identification/Output/1.jpg", image)

    x = out[0]['left']
    y = out[0]['bottom']
    w = out[-1]['right']
    h = out[-1]['top']

    print("Bounded values for Answer :", [x, y, w, h])

    answer = " ".join(text_all)

    fuzz.ratio(value.lower(), answer.lower())