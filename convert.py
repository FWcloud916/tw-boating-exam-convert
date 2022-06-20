# Read pdf.
import json
from pathlib import Path
from pprint import pprint

from PyPDF2 import PdfReader


def convert():
    answer_pattern = ['( A )', '( B )', '( C )', '( D )']
    answer_map = {
        '( A )': 'A',
        '( B )': 'B',
        '( C )': 'C',
        '( D )': 'D'
    }

    options_map = {
        '(A)': 'A',
        '(B)': 'B',
        '(C)': 'C',
        '(D)': 'D'
    }

    category_map = {
        '氣（海）象常識-氣（海）象常識': 'weather-common',
        '海事法規-汙染、走私、毒品等': 'law-crime',
        '海事法規-海洋保育': 'law-sea',
        '海事法規-船員證照資格等': 'law-cert',
        '海事法規-船舶檢丈等': 'law-boat',
        '航海常識-特殊性及駕駛知識與作為': 'sail-common-way',
        '航海常識-航儀及航路標誌': 'sail-common-mark',
        '船機常識-內燃機基本知識': 'sail-common-engine',
        '船機常識-操作運轉': 'sail-common-operate',
        '船機常識-維修保養故障排除': 'sail-common-maintain',
        '船藝與操船-小船之認識': 'seamanship-basic',
        '船藝與操船-甲板設備與繩索': 'seamanship-equip',
        '船藝與操船-航行規劃與技術': 'seamanship-tech',
        '通訊與緊急措施-各種應變': 'communication-management',
        '通訊與緊急措施-緊急對策': 'communication-emergency',
        '避碰規則-各種航法': 'sail-way',
        '避碰規則-燈號、號標、號笛、旗號': 'sail-light'
    }
    result = {}
    categories = {}
    category = ''

    path = Path('clean/1110210.txt')
    num = 0
    answer = ''

    for line in open(path).readlines():
        text = line.strip()

        if not text:
            continue

        if '## ' in text:
            if category:
                categories[category] = len(result[category])

            category_key = text.replace('## ', '')
            category = category_map[category_key]
            result[category] = {}
            continue

        if text in answer_pattern:
            answer = answer_map[text]
            continue

        if text.isnumeric():
            num = int(text)
            result[category][num] = {
                'question': '',
                'A': '',
                'B': '',
                'C': '',
                'D': '',
                'answer': answer,
                'img': ''
            }
            continue

        if text.split(' ')[0] in options_map:
            option_key = options_map[text.split(' ')[0]]
            result[category][num][option_key] = text
            continue

        if '[img]' in text:
            result[category][num]['img'] = text.replace('[img]', '')
            continue

        result[category][num]['question'] = text

    with Path('output/1110210_exam.json').open('w', encoding='utf-8') as f:
        f.write(
            json.dumps(
                result,
                ensure_ascii=False,
                indent=4
            )
        )

    with Path('output/1110210_category.json').open('w', encoding='utf-8') as f:
        f.write(
            json.dumps(
                categories,
                ensure_ascii=False,
                indent=4
            )
        )

    with Path('output/1110210_category_mapping.json').open('w', encoding='utf-8') as f:
        f.write(
            json.dumps(
                {v: k for k, v in category_map.items()},
                ensure_ascii=False,
                indent=4
            )
        )


if __name__ == '__main__':
    convert()
