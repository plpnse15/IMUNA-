import pandas as pd
from django.core.management.base import BaseCommand
from identifier.models import Tree
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Import trees from an Excel file into the database'

    def handle(self, *args, **kwargs):
        # 프로젝트의 최상위 경로(BASE_DIR)를 기준으로 파일 경로를 설정합니다.
        excel_file = os.path.join(settings.BASE_DIR, 'trees.xlsx')
        try:
            df = pd.read_excel(excel_file, dtype=object).fillna('')
            df.columns = [
                'sujong', 'gwa', 'leaf_shape_overall', 'form', 'leaf_shape_detail',
                'leaf_length', 'leaf_arrangement', 'leaf_margin', 'leaf_margin_detail',
                'sting_feel', 'special_notes', 'leaf_tip', 'petiole', 'vein',
                'height', 'fruit_flower'
            ]

            Tree.objects.all().delete() # 기존 데이터 삭제

            for _, row in df.iterrows():
                Tree.objects.create(**row.to_dict())

            self.stdout.write(self.style.SUCCESS(f'Successfully imported data from {excel_file}'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'Error: "{excel_file}" not found.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))
